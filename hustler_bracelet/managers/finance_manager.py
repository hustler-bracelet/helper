# -*- coding: utf-8 -*-

import random

from datetime import date, datetime, timedelta
from typing import Sequence, NoReturn

from sqlalchemy import delete
from sqlalchemy.sql.functions import func
from sqlmodel import select

from hustler_bracelet.bot.utils.lang_utils import format_money_amount
from hustler_bracelet.database.category import Category
from hustler_bracelet.database.exceptions import CategoryAlreadyExistsError, CategoryNotFoundError, TaskNotFoundError
from hustler_bracelet.database.finance_transaction import FinanceTransaction
from hustler_bracelet.database.task import Task
from hustler_bracelet.database.user import User
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.managers.user_manager import UserManager


def create_int_uid() -> int:
    return int(''.join([str(random.randint(0, 9)) for _ in range(9)]))


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
            id=create_int_uid(),
            telegram_id=self._user_manager.telegram_id,
            type=category.type,
            category=category.id,
            value=value,
            added_on=datetime.now(),
            transaction_date=transaction_date
        )
        self._session.add(finance_transaction)

        user = (
            await self._session.exec(
                select(User).where(User.telegram_id == self._user_manager.telegram_id)
            )
        ).first()
        if category.type is FinanceTransactionType.INCOME:
            user.current_balance += value
        else:
            user.current_balance -= value

        await self._session.commit()

    async def get_sum_of_finance_transactions_of_category(self, category: Category) -> float:
        finance_transactions_sum = (
            await self._session.exec(
                select(func.sum(FinanceTransaction.value)).where(
                    FinanceTransaction.category == category.id
                )
            )
        ).one()

        return finance_transactions_sum or 0.

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
            id=create_int_uid(),
            telegram_id=self._user_manager.telegram_id,
            name=name,
            added_on=datetime.now(),
            planned_complete_date=planned_complete_date
        )

        self._session.add(task)
        await self._session.commit()

        return task

    async def mark_tasks_as_completed(self, tasks: Sequence[Task] | Sequence[int]):
        if isinstance(tasks[0], int):
            tasks: Sequence[int]
            tasks: Sequence[Task] = [await self.get_task_by_id(task_id) for task_id in tasks]

        for task in tasks:
            task.is_completed = True

        await self._session.commit()

    async def get_tasks_filtered_by_planned_complete_date(self, planned_complete_date: date, *, completed: bool | None = False) -> Sequence[Task]:
        query = select(Task).where(
            Task.planned_complete_date == planned_complete_date
        )
        if completed is not None:
            query = query.where(
                Task.is_completed == completed
            )

        tasks = (await self._session.exec(query)).all()

        return tasks

    async def get_active_tasks(self) -> Sequence[Task]:
        query = select(Task).where(
            Task.telegram_id == self._user_manager.telegram_id
        )
        query = query.where(Task.is_completed == 0)  # FIXME HACK TODO XXX: this shit aint working if using not stmt
        return (await self._session.exec(query)).all()

    async def get_amount_of_tasks_filtered_by_planned_complete_date(self, planned_complete_date: date, *, completed: bool | None) -> Sequence[Task]:
        query = select(func.count(Task.id)).where(
            Task.planned_complete_date == planned_complete_date,
        )
        if completed is not None:
            query = query.where(
                Task.is_completed == completed
            )

        amount = (await self._session.exec(query)).one()

        return amount

    async def get_amount_of_tasks(self, *, completed: bool | None):
        query = select(func.count(Task.id)).where(
            Task.telegram_id == self._user_manager.telegram_id
        )

        if completed is not None:
            query = query.where(
                Task.is_completed == completed
            )

        amount = (await self._session.exec(query)).one()

        return amount

    async def get_tasks_sorted_by_planned_complete_date(self, *, completed: bool | None = False, limit: int | None = None) -> Sequence[Task]:
        query = select(Task).where(
            Task.telegram_id == self._user_manager.telegram_id
        )

        if completed is not None:
            query = query.where(
                Task.is_completed == completed
            )

        if limit is not None:
            query = query.limit(limit)

        query = query.order_by(Task.planned_complete_date.asc())

        tasks = (await self._session.exec(query)).all()

        return tasks

    async def get_tasks_after_date(self, after_date: date, *, completed: bool | None = False):
        query = select(Task).where(
            Task.telegram_id == self._user_manager.telegram_id,
            Task.planned_complete_date > after_date,
        )
        if completed is not None:
            query = query.where(
                Task.is_completed == completed
            )

        tasks = (await self._session.exec(query)).all()

        return tasks

    async def get_most_profitable_income_category(self) -> tuple[Category, float]:
        category_to_income_map: dict[Category, float] = {}

        for category in await self.get_all_categories(FinanceTransactionType.INCOME):
            category_name = await category.awaitable_attrs.name
            category_total_income = await self.get_sum_of_finance_transactions_of_category(category)
            category_to_income_map[category_name] = category_total_income

        categories_sorted_by_income = sorted(
            category_to_income_map.items(),
            key=lambda x: x[1]+1,
            reverse=True
        )

        category_and_income = categories_sorted_by_income[0]

        return category_and_income[0], category_and_income[1]

    async def get_most_spending_category(self) -> tuple[Category, float]:
        category_to_spendings: dict[Category, float] = {}

        for category in await self.get_all_categories(FinanceTransactionType.SPENDING):
            category_name = await category.awaitable_attrs.name
            category_total_spent = await self.get_sum_of_finance_transactions_of_category(category)
            category_to_spendings[category_name] = category_total_spent

        categories_sorted_by_spendings = sorted(
            category_to_spendings.items(),
            key=lambda x: x[1]+1,
            reverse=True
        )

        category_and_spendings = categories_sorted_by_spendings[0]

        return category_and_spendings[0], category_and_spendings[1]

    async def get_stats_for_time_range(
            self,
            type_: FinanceTransactionType,
            until_date: timedelta
    ) -> tuple[float, int]:
        query = select(FinanceTransaction).where(
            FinanceTransaction.telegram_id == self._user_manager.telegram_id,
            (date.today() - FinanceTransaction.transaction_date) is until_date,
            FinanceTransaction.type == type_
        )
        results = (await self._session.exec(query)).all()

        summed_up_amount = sum([result.value for result in results])
        operations_count = len(results)

        return summed_up_amount, operations_count
