import operator

from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Cancel, Button, Multiselect, Column, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.managers import FinanceManager


async def assets_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    return {
        'assets': [
            (await asset.awaitable_attrs.name, await asset.awaitable_attrs.id)
            for asset in await finance_manager.get_all_assets()
            # TODO: Добавить прогрузку задач по частям, чтобы не грузить каждый раз все сто тыщ мильонов тасок
        ]
    }


async def on_complete_selected_assets_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    finance_manager: FinanceManager = manager.middleware_data['finance_manager']
    assets_multiselect_widget: Multiselect = manager.find('mltslct_assets_to_delete')
    deleted_assets_ids: list[int] = [*map(int, assets_multiselect_widget.get_checked())]

    if not deleted_assets_ids:
        await callback.answer('Выберите хотя бы один актив')
        return

    for asset in deleted_assets_ids:
        await finance_manager.delete_asset(asset)

    await manager.done()


delete_assets_dialog = Dialog(
    Window(
        Const(
            '➖ <b>Удаление активов</b>\n'
            '\n'
            'Выбери активы, которые хочешь удалить:'
        ),
        ScrollingGroup(
            Column(
                Multiselect(
                    Format("✓ {item[0]}"),
                    Format("{item[0]}"),
                    id="mltslct_assets_to_delete",
                    item_id_getter=operator.itemgetter(1),
                    items="assets",
                )
            ),
            id='scrl_assets_to_delete',
            width=1,
            height=6,
            hide_on_single_page=True
        ),
        Row(
            Cancel(
                Const('❌ Отмена')
            ),
            Button(
                Const('✅ Выполнить'),
                id='delete_selected_assets',
                on_click=on_complete_selected_assets_click
            )
        ),
        state=states.DeleteAssets.MAIN,
        getter=assets_getter
    )
)
