from enum import Enum


class FinanceTransactionType(str, Enum):
    INCOME = 'income'
    SPENDING = 'spending'
