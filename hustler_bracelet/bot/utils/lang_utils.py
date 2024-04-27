from aiogram_dialog import DialogManager

from hustler_bracelet.bot.utils import get_event_type
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.finance.manager import FinanceManager


def get_finance_event_type_name(finance_event_type: FinanceTransactionType):
    mapping = {
        FinanceTransactionType.SPENDING: 'расход',
        FinanceTransactionType.INCOME: 'доход',
    }
    return mapping[finance_event_type]


def get_finance_event_type_verb(finance_event_type: FinanceTransactionType):
    mapping = {
        FinanceTransactionType.SPENDING: 'потратил',
        FinanceTransactionType.INCOME: 'заработал',
    }
    return mapping[finance_event_type]


def get_finance_event_type_emoji(finance_event_type: FinanceTransactionType):
    mapping = {
        FinanceTransactionType.SPENDING: '💳',
        FinanceTransactionType.INCOME: '🤑',
    }
    return mapping[finance_event_type]


async def finance_event_words_getter(dialog_manager: DialogManager, **kwargs):
    event_type = get_event_type(dialog_manager)

    words = {
        'finance_event_name': get_finance_event_type_name(event_type),
        'finance_event_verb': get_finance_event_type_verb(event_type),
        'finance_event_emoji': get_finance_event_type_emoji(event_type),
    }

    capitalized_words = {}

    for key, value in words.items():
        capitalized_words[f'capitalized_{key}'] = value.capitalize()

    return {**words, **capitalized_words}


def format_money_amount(money_amount: float) -> str:
    if money_amount.is_integer():
        money_amount = int(money_amount)
    spaced_money_amount = f'{money_amount:_}'.replace('_', ' ')  # КОСТЫЛИ ЕБУЧИЕ

    return f'{spaced_money_amount}₽'


async def formatted_balance_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    raw_balance = await finance_manager.get_balance()
    formatted_balance = format_money_amount(raw_balance)

    return {
        'balance': formatted_balance
    }


async def formatted_event_value_getter(dialog_manager: DialogManager, **kwargs):
    raw_value = dialog_manager.dialog_data['value']
    formatted_value = format_money_amount(raw_value)

    return {
        'value': formatted_value
    }
