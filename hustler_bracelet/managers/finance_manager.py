# -*- coding: utf-8 -*-

from datetime import date, datetime
from typing import Sequence, NoReturn
from uuid import uuid4 as create_uuid_v4

from sqlalchemy.sql.functions import func
from sqlmodel import select

from hustler_bracelet.database.category import Category
from hustler_bracelet.database.exceptions import CategoryAlreadyExistsError, CategoryNotFoundError
from hustler_bracelet.database.finance_transaction import FinanceTransaction
from hustler_bracelet.database.user import User
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.managers.user_manager import UserManager


class FinanceManager:
    def __init__(self, user_manager: UserManager):
        self._user_manager = user_manager
        self._session = user_manager.get_database_session()

    async def get_balance(self) -> float:
        user = (await self._session.exec(
            select(User).where(User.telegram_id == self._user_manager.telegram_id)
        )).first()
        return user.current_balance

    async def get_all_categories(self, category_type: FinanceTransactionType) -> Sequence[Category]:
        query_results = (await self._session.exec(
            select(Category).where(
                Category.telegram_id == self._user_manager.telegram_id,
                Category.type == category_type
            )
        )).all()
        print(category_type)
        return query_results

    async def get_all_events(self, category_type: FinanceTransactionType) -> Sequence[FinanceTransaction]:
        query_results = (await self._session.exec(
            select(FinanceTransaction).where(
                FinanceTransaction.telegram_id == self._user_manager.telegram_id,
                FinanceTransaction.type == category_type
            )
        )).all()
        return query_results

    async def get_events_amount(self, category_type: FinanceTransactionType) -> int:
        query_results = (await self._session.exec(
            select(func.count(FinanceTransaction.id)).where(
                FinanceTransaction.telegram_id == self._user_manager.telegram_id,
                FinanceTransaction.type == category_type
            )
        )).one()
        return query_results

    async def get_categories_amount(self, category_type: FinanceTransactionType) -> int:
        query_results = (await self._session.exec(
            select(func.count(Category.id)).where(
                Category.telegram_id == self._user_manager.telegram_id,
                Category.type == category_type
            )
        )).one()
        return query_results

    async def create_new_category(self, name: str, category_type: FinanceTransactionType) -> Category:
        # Check if this user already has categories with the same name and type
        categories_with_same_name = (await self._session.exec(
            select(Category).where(
                Category.name == name,
                Category.telegram_id == self._user_manager.telegram_id,
                Category.type == category_type
            )
        )).all()
        if categories_with_same_name:
            raise CategoryAlreadyExistsError()

        # Create the category
        new_category = Category(
            telegram_id=self._user_manager.telegram_id,
            name=name,
            type=category_type
        )
        self._session.add(new_category)
        await self._session.commit()

        return new_category

    async def delete_category(self, category_to_delete: Category):
        await self._session.delete(category_to_delete)
        await self._session.commit()

    async def add_finance_transaction(self, category: Category, value: int | float, transaction_date: date = date.today()):
        value = float(value)

        finance_transaction = FinanceTransaction(
            id=str(create_uuid_v4()),
            telegram_id=self._user_manager.telegram_id,
            type=category.type,
            category=category.id,
            value=value,
            added_on=datetime.now(),
            transaction_date=transaction_date
        )
        self._session.add(finance_transaction)

        user = (await self._session.exec(
            select(User).where(User.telegram_id == self._user_manager.telegram_id)
        )).first()
        if category.type is FinanceTransactionType.INCOME:
            user.current_balance += value
        else:
            user.current_balance -= value

        await self._session.commit()

        return

    async def get_category_by_id(self, id_: int) -> Category | NoReturn:
        category = (await self._session.exec(select(Category).where(Category.id == id_))).first()

        if category is None:
            raise CategoryNotFoundError()

        return category
