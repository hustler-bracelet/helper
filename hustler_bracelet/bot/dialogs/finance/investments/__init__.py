from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Row, Cancel
from aiogram_dialog.widgets.text import Format, Const

from hustler_bracelet.bot.dialogs import states

investments_main_menu_dialog = Dialog(
    Window(
        Format(
            '📊 <b>Инвестиции</b>\n'
            '\n'
            '💵 <b>Всего в активах:</b> Soon..\n'
            '🧮 Твой капитал на Soon..% состоит из активов\n'
            '\n'
            '📈 <b>Твои активы:</b>\n'
            ' •  Soon..\n'
            '\n'
            '🕐 <b>История зачислений:<b>\n'
            'Soon..\n'
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
        Cancel(Const('❌ Отмена')),
        state=states.FinanceInvestmentsMenu.MAIN
    )
)
