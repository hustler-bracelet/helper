from aiogram_dialog import Dialog, LaunchMode, Window, StartMode
from aiogram_dialog.about import about_aiogram_dialog_button
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const
from . import states
from ...enums import FinanceEventType

main_dialog = Dialog(
    Window(
        Const(
            '👋 **Привет, хаслер!**\n'
            'Вот твоя сводка на сегодня:\n'
            '\n'
            '💵 **Твой капитал:** 550 000₽\n'
            '• Сегодня было 2 прихода и 0 расходов\n'
            '\n'
            '📝 **2 задачи на сегодня:**\n'
            '• Налить трафа Ване\n'
            '• Вынести мусор\n'
            '\n'
            '🕔 **И ещё 1 задача на завтра:**\n'
            '• Инвайт на фотостудию\n'
        ),
        Start(
            text=Const("📐 Layout widgets"),
            id="layout",
            state=states.Layouts.MAIN,
        ),
        Start(
            text=Const("📜 Scrolling widgets"),
            id="scrolls",
            state=states.Scrolls.MAIN,
        ),
        Start(
            text=Const("☑️ Selection widgets"),
            id="selects",
            state=states.Selects.MAIN,
        ),
        Start(
            text=Const("🤑 Добавить доход"),
            id="add_income",
            state=states.AddFinanceEvent.MAIN,
            data={'event_type': FinanceEventType.INCOME}
        ),
        Start(
            text=Const("💳 Добавить расход"),
            id="add_spend",
            state=states.AddFinanceEvent.MAIN,
            data={'event_type': FinanceEventType.SPEND}
        ),
        Start(
            text=Const("💯 Counter and Progress"),
            id="counter",
            state=states.Counter.MAIN,
        ),
        Start(
            text=Const("🎛 Combining widgets"),
            id="multiwidget",
            state=states.Multiwidget.MAIN,
        ),
        Start(
            text=Const("🔢 Multiple steps"),
            id="switch",
            state=states.Switch.MAIN,
        ),
        Start(
            text=Const("⌨️ Reply keyboard"),
            id="reply",
            state=states.ReplyKeyboard.MAIN,
        ),
        about_aiogram_dialog_button(),
        state=states.Main.MAIN,
    ),
    launch_mode=LaunchMode.ROOT,
)
