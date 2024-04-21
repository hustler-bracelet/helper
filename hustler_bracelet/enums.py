from enum import Enum


class FinanceEventType(str, Enum):
    INCOME = 'income'
    SPEND = 'spend'


# TODO(nsdkin): УДАЛИТЬ К ХУЯМ
# есть database.FinanceTransactionType
# но мб его нужно переименовать в что-то менее длинное и сложное
