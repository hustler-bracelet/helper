from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Row, Cancel
from aiogram_dialog.widgets.text import Format, Const

from hustler_bracelet.bot.dialogs import states

investments_main_menu_dialog = Dialog(
    Window(
        Format(
            '📊 <b>Инвестиции</b>\n'
            '\n'
            '💵 <b>Всего в активах:</b> 267 812₽\n'
            '🧮 Твой капитал на 48.69% состоит из активов\n'
            '\n'
            '📈 <b>Твои активы:</b>\n'
            ' •  <b>Нак. счёт Сбер:</b> 215 000₽ (15%, прибыль: 15 000₽)\n'
            ' •  <b>Браслет токен:</b> 52 812₽ (прибыль: 2 812₽)\n'
            '\n'
            '🕐 <b>История зачислений:<b>\n'
            '26.04.2024 + 5 000₽ по активу Нак. счёт Сбер\n'
            '26.03.2024 + 5 000₽ по активу Нак. счёт Сбер\n'
            '02.03.2024 + 2 812₽ по активу Браслет токен\n'
            '26.02.2024 + 5 000₽ по активу Нак. счёт Сбер'
        ),
        Start(
            Const('🤑 Добавить прибыль'),
            id='add_asset_income',
            state=NotImplemented
        ),
        Row(
            Start(
                Const('➕ Добавить актив'),
                id='add_asset',
                state=NotImplemented
            ),
            Start(
                Const('➖ Удалить актив'),
                id='delete_asset',
                state=NotImplemented
            ),
        ),
        Row(
            Start(
                Const('✏️ Переим. актив'),
                id='rename_asset',
                state=NotImplemented
            ),
            Start(
                Const('🧮 Изменить % ставку'),
                id='change_asset_percent',
                state=NotImplemented
            ),
        ),
        Cancel(),
        state=states.FinanceInvestmentsMenu.MAIN
    )
)
