from aiogram_dialog import DialogManager

from hustler_bracelet.enums import FinanceTransactionType

__all__ = ('get_event_type',)


def get_event_type(dialog_manager: DialogManager) -> FinanceTransactionType:
    event_type = None

    if dialog_manager.dialog_data:
        event_type = dialog_manager.dialog_data.get('cat_type') or dialog_manager.dialog_data.get('event_type')
    if dialog_manager.start_data:
        event_type = dialog_manager.start_data.get('cat_type') or dialog_manager.start_data.get('event_type')

    if event_type is None:
        raise ValueError('Не удалось понять из контекста, о каком типе ивента (категории) идёт речь.\n'
                         f'Текущее состояние окна диалога: {dialog_manager.current_context().state}')

    return event_type
