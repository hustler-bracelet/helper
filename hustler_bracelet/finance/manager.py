# -*- coding: utf-8 -*-
from datetime import date, datetime
from typing import Sequence, NoReturn
from uuid import uuid4 as create_uuid_v4

from sqlmodel.ext.asyncio.session import AsyncSession

from hustler_bracelet.database.engine import DATABASE_ENGINE
from hustler_bracelet.database.exceptions import CategoryAlreadyExistsError, CategoryNotFoundError
from hustler_bracelet.database.user import User
from hustler_bracelet.database.category import Category
from hustler_bracelet.database.finance_transaction import FinanceTransaction
from sqlmodel import Session, select

from hustler_bracelet.enums import FinanceTransactionType


class FinanceManager:
    def __init__(self, telegram_id: int):
        self._telegram_id = telegram_id
        self._session = AsyncSession(DATABASE_ENGINE)

    async def _is_user_exists(self):
        query_result = (await self._session.exec(
            select(User).where(User.telegram_id == self._telegram_id)
        )).all()
        return bool(query_result)

    async def _create_new_user(self, telegram_name: str):
        assert not await self._is_user_exists()

        new_user = User(
            telegram_id=self._telegram_id,
            telegram_name=telegram_name,
            current_balance=0.0
        )
        self._session.add(new_user)
        await self._session.commit()

        return new_user

    async def create_user_if_not_exists(self, telegram_name: str):
        if not await self._is_user_exists():
            await self._create_new_user(telegram_name)

    async def get_balance(self) -> float:
        user = (await self._session.exec(
            select(User).where(User.telegram_id == self._telegram_id)
        )).first()
        return user.current_balance

    async def get_all_categories(self, category_type: FinanceTransactionType) -> Sequence[Category]:
        query_results = (await self._session.exec(
            select(Category).where(
                Category.telegram_id == self._telegram_id
                and Category.type == category_type
            )
        )).all()
        return query_results

    async def create_new_category(self, name: str, category_type: FinanceTransactionType) -> Category:
        # Check if this user already has categories with the same name and type
        categories_with_same_name = (await self._session.exec(
            select(Category).where(
                Category.name == name
                and Category.telegram_id == self._telegram_id
                and Category.type == category_type
            )
        )).all()
        if categories_with_same_name:
            raise CategoryAlreadyExistsError()

        # Create the category
        new_category = Category(
            uuid=str(create_uuid_v4()),
            telegram_id=self._telegram_id,
            name=name,
            type=category_type
        )
        self._session.add(new_category)
        await self._session.commit()

        return new_category

    async def delete_category(self, category_to_delete: Category):
        await self._session.delete(category_to_delete)
        await self._session.commit()

    async def add_income(self, category: Category, value: int | float, transaction_date: date = date.today()):
        value = float(value)

        finance_transaction = FinanceTransaction(
            uuid=str(create_uuid_v4()),
            telegram_id=self._telegram_id,
            type=FinanceTransactionType.INCOME,
            category=category.uuid,
            value=value,
            added_on=datetime.now(),
            transaction_date=transaction_date
        )
        self._session.add(finance_transaction)

        user = (await self._session.exec(
            select(User).where(User.telegram_id == self._telegram_id)
        )).first()
        user.current_balance += value

        await self._session.commit()

        return

    async def get_category_by_id(self, id_: str) -> Category | NoReturn:
        category = (await self._session.exec(select(Category).where(Category.uuid == id_))).first()

        if category is None:
            raise CategoryNotFoundError()

        return category

    async def __aenter__(self):
        return await self._session.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._session.__aexit__(exc_type, exc_val, exc_tb)
