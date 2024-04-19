from enum import Enum


class FinanceEventType(str, Enum):
    INCOME = 'income'
    SPEND = 'spend'
