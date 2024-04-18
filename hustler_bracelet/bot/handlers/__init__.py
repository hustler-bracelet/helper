from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from hustler_bracelet.bot.keyboards.main_menu import get_main_menu_kb

from .finance import router as finance_router
from .sport import router as sport_router
from .tasks import router as tasks_router

router = Router()
router.include_routers(
    finance_router,
    sport_router,
    tasks_router
)


@router.message(F.text.startswith('/start'))
async def cmd_start(message: types.Message):
    await message.answer(
        'Привет! Я твой помощник в мире капитализма. '
        'Тут ты можешь проводить анализ финансов, записывать и распределять задачи, '
        'а так же следить за своим питанием и составлять графики тренировок. '
        'Буду давать тебе простенькие рекомендации на все эти темы.',
        reply_markup=get_main_menu_kb()
    )


@router.message(F.text.startswith('/cancel'))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer('Контекст успешно сброшен.')

    await cmd_start(message)
