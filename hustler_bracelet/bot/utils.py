from aiogram_dialog import DialogManager

from hustler_bracelet.enums import FinanceEventType


def get_finance_event_type_name(finance_event_type: FinanceEventType):
    mapping = {
        FinanceEventType.SPEND: 'трат',
        FinanceEventType.INCOME: 'доходов',
    }
    return mapping[finance_event_type]


async def finance_event_name_getter(dialog_manager: DialogManager, **kwargs):
    event_type = dialog_manager.start_data.get('event_type') or dialog_manager.start_data.get('cat_type')

    try:
        return {'finance_event_name': get_finance_event_type_name(event_type)}
    except KeyError:
        return {'finance_event_name': 'хз что сделал'}
