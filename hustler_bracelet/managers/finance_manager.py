# -*- coding: utf-8 -*-

from datetime import date, datetime
from typing import Sequence, NoReturn
from uuid import uuid4 as create_uuid_v4

from sqlalchemy import delete
from sqlalchemy.sql.functions import func
from sqlmodel import select

from hustler_bracelet.database.category import Category
from hustler_bracelet.database.exceptions import CategoryAlreadyExistsError, CategoryNotFoundError, TaskNotFoundError
from hustler_bracelet.database.finance_transaction import FinanceTransaction
from hustler_bracelet.database.task import Task
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

    async def delete_category(self, category_to_delete: Category, delete_related_events: bool = True):
        if delete_related_events:
            await self._session.exec(
                delete(FinanceTransaction).
                where(
                    FinanceTransaction.category == category_to_delete.id
                )
            )

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

    async def get_category_by_id(self, id_: int) -> Category | NoReturn:
        category = (await self._session.exec(select(Category).where(Category.id == id_))).first()

        if category is None:
            raise CategoryNotFoundError()

        return category

    async def get_task_by_id(self, id_: int) -> Task | NoReturn:
        task = (await self._session.exec(select(Task).where(Task.id == id_))).first()

        if task is None:
            raise TaskNotFoundError()

        return task

    async def add_task(self, name: str, planned_complete_date: date):
        task = Task(
            telegram_id=self._user_manager.telegram_id,
            name=name,
            added_on=datetime.now(),
            planned_complete_date=planned_complete_date
        )
        self._session.add(task)

        await self._session.commit()

    async def mark_tasks_as_completed(self, tasks: Sequence[Task] | Sequence[int]):
        if isinstance(tasks[0], int):
            tasks: Sequence[int]
            tasks: Sequence[Task] = [await self.get_task_by_id(task_id) for task_id in tasks]

        for task in tasks:
            task.is_completed = True

        await self._session.commit()

    async def get_tasks_filtered_by_planned_complete_date(self, planned_complete_date: date, excluding_completed: bool = True) -> Sequence[Task]:
        query = select(Task).where(
            Task.planned_complete_date == planned_complete_date,

        )
        if excluding_completed:
            query = query.where(
                Task.is_completed == False
            )

        tasks = (await self._session.exec(query)).all()

        return tasks

    async def get_tasks_sorted_by_planned_complete_date(self, excluding_completed: bool = True, limit: int | None = None) -> Sequence[Task]:
        query = select(Task)

        if excluding_completed:
            query = query.where(
                Task.is_completed == False
            )

        if limit is not None:
            query = query.limit(limit)

        query = query.order_by(Task.planned_complete_date.asc())

        tasks = (await self._session.exec(query)).all()

        return tasks

    async def get_tasks_after_date(self, after_date: date, excluding_completed: bool = True):
        query = select(Task).where(
            Task.planned_complete_date > after_date,
        )
        if excluding_completed:
            query = query.where(
                Task.is_completed == False
            )

        tasks = (await self._session.exec(query)).all()

        return tasks
