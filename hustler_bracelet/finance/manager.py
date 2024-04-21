# -*- coding: utf-8 -*-

from typing import Sequence
from uuid import uuid4 as create_uuid_v4

from hustler_bracelet.database.engine import DATABASE_ENGINE
from hustler_bracelet.database.exceptions import CategoryAlreadyExists
from hustler_bracelet.database.user import User
from hustler_bracelet.database.category import Category, FinanceTransactionType
from sqlmodel import Session, select


class FinanceManager:
    def __init__(self, telegram_id: int, telegram_name: str):
        self._telegram_id = telegram_id
        self._session = Session(DATABASE_ENGINE)
        if not self._is_user_existing():
            self._create_new_user(telegram_name)

    def _is_user_existing(self):
        with self._session:
            query_result = self._session.exec(
                select(User).where(User.telegram_id == self._telegram_id)
            ).all()
            return bool(query_result)

    def _create_new_user(self, telegram_name: str):
        assert not self._is_user_existing()
        with self._session:
            new_user = User(
                telegram_id=self._telegram_id,
                telegram_name=telegram_name,
                current_balance=0.0
            )
            self._session.add(new_user)
            self._session.commit()
        return new_user

    def get_all_categories(self, category_type: FinanceTransactionType) -> Sequence[Category]:
        with self._session:
            query_results = self._session.exec(
                select(Category).where(
                    Category.telegram_id == self._telegram_id
                    and Category.type == category_type
                )
            ).all()
            print(query_results)
        return query_results

    def create_new_category(self, name: str, category_type: FinanceTransactionType) -> Category:
        with self._session:
            # Check if this user already has categories with the same name and type
            categories_with_same_name = self._session.exec(
                select(Category).where(
                    Category.name == name
                    and Category.telegram_id == self._telegram_id
                    and Category.type == category_type
                )
            ).all()
            if categories_with_same_name:
                raise CategoryAlreadyExists

            # Create the category
            new_category = Category(
                uuid=str(create_uuid_v4()),
                telegram_id=self._telegram_id,
                name=name,
                type=category_type
            )
            self._session.add(new_category)
            self._session.commit()
        return new_category

    def delete_category(self, category_to_delete: Category):
        with self._session:
            self._session.delete(category_to_delete)
            self._session.commit()
