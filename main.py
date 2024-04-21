from __future__ import annotations

import asyncio

from hustler_bracelet import bot
from hustler_bracelet.database.engine import create_all_tables
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.finance.manager import FinanceManager


create_all_tables()
finance_manager = FinanceManager(telegram_id=6567176437, telegram_name='Дмитрий')
all_categories = finance_manager.get_all_categories(category_type=FinanceTransactionType.INCOME)
print(finance_manager.get_balance())
finance_manager.add_income(
    category=all_categories[0],
    value=1500
)
print(finance_manager.get_balance())


exit()
asyncio.run(bot.main())
