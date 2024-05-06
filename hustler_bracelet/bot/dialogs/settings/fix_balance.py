from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Jinja, Format, Const

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.dialogs.widgets import NumberInput
from hustler_bracelet.managers import FinanceManager


async def fix_balance_menu_dialog_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    return {
        'balance': await finance_manager.get_balance(),
    }


async def get_sum_for_balance_fixing(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: float
):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    balance = (await finance_manager.get_balance()) + data
    await finance_manager.set_balance(balance)

    await dialog_manager.next()


fix_balance_menu_dialog = Dialog(
    Window(
        Jinja(
            '🛠 <b>Изменение баланса</b>\n'
            '\n'
            'Сейчас твой баланс составляет {{ balance|money }}. Сколько ты хочешь прибавить к нему?\n'
            '<span class="tg-spoiler">Интересно, а что будет, если прибавить отрицательное число?</span>'
        ),
        NumberInput(on_success=get_sum_for_balance_fixing),
        Cancel(Const('❌ Отмена')),
        state=states.FixBalance.MAIN,
    ),
    Window(
        Jinja(
            '🛠 <b>Изменение баланса</b>\n'
            '\n'
            'Отлично! Теперь твой баланс составляет {{ balance|money }}'
        ),
        Cancel(Const('👌 Ок')),
        state=states.FixBalance.FINAL
    ),
    getter=fix_balance_menu_dialog_getter,
)
