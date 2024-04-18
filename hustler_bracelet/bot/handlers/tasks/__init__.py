from aiogram import Router, F, types

router = Router()


@router.callback_query(F.data == 'tasks_menu')
async def ibtn_finance_menu(call: types.CallbackQuery):
    await call.answer('Soon..')
