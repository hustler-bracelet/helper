from aiogram_dialog import DialogManager

from hustler_bracelet.enums import FinanceEventType


def get_finance_event_type_name(finance_event_type: FinanceEventType):
    mapping = {
        FinanceEventType.SPEND: 'расход',
        FinanceEventType.INCOME: 'доход',
    }
    return mapping[finance_event_type]


def get_finance_event_type_verb(finance_event_type: FinanceEventType):
    mapping = {
        FinanceEventType.SPEND: 'потратил',
        FinanceEventType.INCOME: 'заработал',
    }
    return mapping[finance_event_type]


def get_finance_event_type_emoji(finance_event_type: FinanceEventType):
    mapping = {
        FinanceEventType.SPEND: '💳',
        FinanceEventType.INCOME: '🤑',
    }
    return mapping[finance_event_type]


async def finance_event_words_getter(dialog_manager: DialogManager, **kwargs):
    event_type = dialog_manager.start_data.get('event_type') or dialog_manager.start_data.get('cat_type')

    words = {
        'finance_event_name': get_finance_event_type_name(event_type),
        'finance_event_verb': get_finance_event_type_verb(event_type),
        'finance_event_emoji': get_finance_event_type_emoji(event_type),
    }

    capitalized_words = {}

    for key, value in words.items():
        capitalized_words[f'capitalized_{key}'] = value.capitalize()

    return {**words, **capitalized_words}
