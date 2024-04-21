from __future__ import annotations

import asyncio

from hustler_bracelet import bot
from hustler_bracelet.database.engine import create_all_tables
from hustler_bracelet.database.finance_transaction_type import FinanceTransactionType
from hustler_bracelet.finance.manager import FinanceManager


create_all_tables()
finance_manager = FinanceManager(telegram_id=6567176437, telegram_name='Дмитрий')
finance_manager.get_all_categories(category_type=FinanceTransactionType.INCOME)
finance_manager.create_new_category(
    name='Тестовая категория дохода',
    category_type=FinanceTransactionType.INCOME
)
finance_manager.create_new_category(
    name='Тестовая категория расхода',
    category_type=FinanceTransactionType.SPENDING
)


exit()
asyncio.run(bot.main())
