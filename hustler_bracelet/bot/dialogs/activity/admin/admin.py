import config
import datetime
import pytz

from aiogram import Router, types, Bot, F
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext

from hustler_bracelet.client import ActivityAPIClient, ActivityTasksAPIClient, ProofsAPIClient
from hustler_bracelet.client.schemas import ActivityDataResponse, ProofResponse, ProofLoadedReasonse
from hustler_bracelet.client.schemas import ActivityTaskCreateData
from hustler_bracelet.bot.dialogs import states

from .utils import SimplePagination


WEB_APP_URL = config.WEB_APP_URL


admin_router = Router()
activity_client = ActivityAPIClient()
activity_task_client = ActivityTasksAPIClient()
proofs_client = ProofsAPIClient()


def get_admin_main_kb(has_activities: bool) -> types.InlineKeyboardMarkup:
    kb = [
        [
            types.InlineKeyboardButton(
                text='⚡️ Запустить активность',
                callback_data='admin:create_activity'
            ),
        ],
    ]

    if has_activities:
        kb.append(
            [
                types.InlineKeyboardButton(
                    text='Управление активностями',
                    callback_data='admin:view_activity'
                ),
            ]
        )

    return types.InlineKeyboardMarkup(inline_keyboard=kb)


@admin_router.callback_query(F.data == 'admin:main')
async def on_admin_main_click(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    return await on_admin_command(callback.message, bot)


@admin_router.message(Command('admin'))
async def on_admin_command(message: types.Message, bot: Bot):
    await message.answer(
        '👋 Здарова, заебал', 
        reply_markup=get_admin_main_kb(True)
    )


def get_webapp_kb(telegram_id: int) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='Открыть форму',
                    web_app=types.WebAppInfo(
                        url=f'{WEB_APP_URL}?telegram_id={telegram_id}')
                ),
            ],
        ]
    )


@admin_router.callback_query(F.data == 'admin:create_activity')
async def create_activity(callback: types.CallbackQuery, bot: Bot):
    await callback.message.edit_text(
        '⚡️ Запуск активности\n\n'
        'Заполни форму в веб-аппке:', 
        reply_markup=get_webapp_kb(
            callback.from_user.id,
        )
    )

# TODO: тут надо подумать над вебаппом


def generate_activiities_choice_kb(activities: list[ActivityDataResponse]) -> types.InlineKeyboardMarkup:
    kb = [
        [
            types.InlineKeyboardButton(
                text=f"{activity.emoji} {activity.name}",
                callback_data=f'admin:activity:{activity.id}'
            ),
        ]
        for activity in activities
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_activity_text(activity: ActivityDataResponse) -> str:
    return f"👋 Здарова, заебал\n\nТекущая акивность: {activity.emoji} {activity.name}"


def get_activity_kb(activity: ActivityDataResponse, pagination) -> types.InlineKeyboardMarkup:
    if pagination:
        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                pagination,
                [
                    types.InlineKeyboardButton(
                        text='➕ Разослать задание',
                        callback_data=f'admin:view_activity:{activity.id}',
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text='Посмотреть пруфы',
                        callback_data=f'admin:main:{activity.id}',
                    ),
                ]
            ]
        )

    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='➕ Разослать задание',
                    callback_data=f'admin:add_task:{activity.id}',
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text='📝 Посмотреть пруфы',
                    callback_data=f'admin:check_proofs:{activity.id}',
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text='❌ Остановить активность',
                    callback_data=f'admin:stop_activity:{activity.id}',
                ),
            ]
        ]
    )


@admin_router.callback_query(F.data == 'admin:view_activity')
async def view_activities(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    activities: list[ActivityDataResponse] = await ActivityAPIClient().get_activities()

    if not activities:
        await callback.message.answer('Нет активностей, выбери создать активность')
        return

    await state.update_data(activities=activities)

    if not activities:
        await callback.message.answer('Нет активностей, выбери создать активность')
        return

    pagination = SimplePagination(
        activities, start_callback='admin:activity'
    )

    current = pagination.get_current_data()

    text = get_activity_text(current)
    kb = get_activity_kb(current, pagination.get_pagination_buttons())

    await callback.message.edit_text(text, reply_markup=kb)


@admin_router.callback_query(F.data.startswith('admin:activity:'))
async def view_activity(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    activities = state_data['activities']

    pagination = SimplePagination(
        activities, start_callback='admin:activity'
    ).load_from_callback_data(callback.data)

    current = pagination.get_current_data()

    text = get_activity_text(current)
    kb = get_activity_kb(current, pagination.get_pagination_buttons())

    await callback.message.edit_text(text, reply_markup=kb)


def get_new_task_text(text: str) -> str:
    return "➕ Рассылка заданий\n\n" + text


def get_niches_kb(activity: ActivityDataResponse):
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text=f"{niche.emoji} {niche.name}",
                callback_data=f'admin:choose_niche:{niche.id}',
            ),
        ]
        for niche in activity.niches
    ])


@admin_router.callback_query(F.data.startswith('admin:add_task:'))
async def add_task(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    activity_id = callback.data.split(':')[-1]

    await state.set_state(states.AdminCreateTask.CHOOSE_NICHE)
    await state.update_data(activity_id=activity_id)

    activity: ActivityDataResponse = await ActivityAPIClient().get_current_activity()

    kb = get_niches_kb(activity)
    text = get_new_task_text('Выбери нишу для рассылки заданий')

    await callback.message.edit_text(text, reply_markup=kb)


@admin_router.callback_query(states.AdminCreateTask.CHOOSE_NICHE, F.data.startswith('admin:choose_niche:'))
async def choose_niche(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    niche_id = callback.data.split(':')[-1]

    await state.update_data(niche_id=niche_id)
    await state.set_state(states.AdminCreateTask.TASK_NAME)

    text = get_new_task_text('Напиши название задания')

    await callback.message.answer(text)


@admin_router.message(states.AdminCreateTask.TASK_NAME)
async def task_name(message: types.Message, state: FSMContext):
    await state.update_data(task_name=message.text)
    await state.set_state(states.AdminCreateTask.TASK_TEXT)

    text = get_new_task_text('Напиши текст задания')

    await message.answer(text)


@admin_router.message(states.AdminCreateTask.TASK_TEXT)
async def task_text(message: types.Message, state: FSMContext):
    await state.update_data(task_text=message.text)
    await state.set_state(states.AdminCreateTask.TASK_POINTS)

    text = get_new_task_text('Напиши кол-во баллов')

    await message.answer(text)


@admin_router.message(states.AdminCreateTask.TASK_POINTS)
async def task_points(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Нужно ввести число')
        return

    await state.update_data(task_points=message.text)
    await state.set_state(states.AdminCreateTask.TASK_DEADLINE)

    text = get_new_task_text('Напиши дедлайн задания, в формате "дд.мм.гггг чч:мм"')

    await message.answer(text)


@admin_router.message(states.AdminCreateTask.TASK_DEADLINE)
async def task_deadline(message: types.Message, state: FSMContext):
    await state.update_data(task_deadline=message.text)

    try:
        deadline = datetime.datetime.strptime(message.text, '%d.%m.%Y %H:%M').astimezone(pytz.timezone('Europe/Moscow'))
    except Exception:
        await message.answer('Нужно ввести дедлайн задания в формате "дд.мм.гггг чч:мм"')
        return

    data = await state.get_data()
    niche_id = data['niche_id']
    task_name = data['task_name']
    task_text = data['task_text']
    task_points = data['task_points']
    task_deadline = deadline

    await activity_task_client.create_new_task(
        niche_id,
        ActivityTaskCreateData(
            name=task_name,
            description=task_text,
            deadline=task_deadline,
            points=int(task_points),
        )
    )

    await state.clear()
    await message.answer(
        'Задание создано!',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Назад к активностям',
                        callback_data='admin:view_activity',
                    ),
                ]
            ]
        ),
    )


def get_proof_text(proof: ProofLoadedReasonse) -> str:
    return (
        f"Доказательство #{proof.id}\n\n"
        f"От: {proof.user.telegram_name}\n"
        f"Задание: {proof.task.name}\n"
        f"Отправил в {proof.sent_on.strftime('%d.%m.%Y %H:%M')}\n"
        f"Комментарий: {proof.caption or '-'}\n"
    )


def generate_proofs_kb(proof_id: int, pagination) -> types.InlineKeyboardMarkup:
    if pagination:
        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                pagination,
                [
                    types.InlineKeyboardButton(
                        text='❌ Отклонить',
                        callback_data=f'admin:reject_proofs:{proof_id}'
                    ),
                    types.InlineKeyboardButton(
                        text='✅ Подтвердить',
                        callback_data=f'admin:accept_proofs:{proof_id}'
                    ),
                ]
            ],
        )
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='❌ Отклонить',
                    callback_data=f'admin:reject_proofs:{proof_id}'
                ),
                types.InlineKeyboardButton(
                    text='✅ Подтвердить',
                    callback_data=f'admin:accept_proofs:{proof_id}'
                ),
            ]
        ],
    )



@admin_router.callback_query(F.data.startswith('admin:check_proofs:'))
async def paginate_proof(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)

    if callback.data.startswith('admin:check_proofs'):
        activity_id = callback.data.split(':')[-1]
    else:
        data = await state.get_data()
        activity_id = data['activity_id']

    await state.update_data(activity_id=activity_id)

    proofs: list[ProofLoadedReasonse] = await proofs_client.get_proofs_waitlist(activity_id)

    if not proofs:
        await callback.answer('Доказательств нет')
        return await view_activities(callback, state)

    await state.update_data(proofs=proofs)

    pagination = SimplePagination(
        proofs,
        start_callback='admin:paginate_proofs',
    )

    current: ProofLoadedReasonse = pagination.get_current_data()

    text = get_proof_text(current)
    kb = generate_proofs_kb(current.id, pagination.get_pagination_buttons())

    if len(current.photo_ids) > 1:
        await callback.message.delete()
        msgs = await bot.send_media_group(
            chat_id=callback.from_user.id,
            media=[
                types.InputMediaPhoto(media=media_id) for media_id in current.photo_ids
            ],
        )

        msgs_ids = [message.message_id for message in msgs]
        await state.update_data(msgs_ids=msgs_ids)

        await callback.message.answer(
            text=text,
            reply_markup=kb,
        )
        return

    elif len(current.photo_ids) == 1:
        await callback.message.delete()
        message = await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=current.photo_ids[0],
            caption=text,
            reply_markup=kb
        )

    await callback.message.delete()
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=text,
        reply_markup=kb
    )


@admin_router.callback_query(F.data.startswith('admin:paginate_proofs:'))
async def paginate_proofs(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    proofs: list[ProofLoadedReasonse] = data['proofs']

    pagination = SimplePagination(
        proofs,
        start_callback='admin:paginate_proofs',
    ).load_from_callback_data(callback.data)

    current: ProofLoadedReasonse = pagination.get_current_data()

    text = get_proof_text(current)
    kb = generate_proofs_kb(current.id, pagination.get_pagination_buttons())

    data = await state.get_data()
    if data.get('msgs_ids'):
        msgs_ids = data['msgs_ids']
        await bot.delete_messages(callback.from_user.id, msgs_ids)
        await state.update_data(msgs_ids=None)

    if len(current.photo_ids) > 1:
        await callback.message.delete()
        messages = await bot.send_media_group(
            chat_id=callback.from_user.id,
            media=[
                types.InputMediaPhoto(media=media_id) for media_id in current.photo_ids
            ],
        )

        msgs_ids = [message.message_id for message in messages]
        await state.update_data(msgs_ids=msgs_ids)

        await callback.message.answer(
            text=text,
            reply_markup=kb,
        )
        return

    elif len(current.photo_ids) == 1:
        await callback.message.delete()
        message = await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=current.photo_ids[0],
            caption=text,
            reply_markup=kb
        )

    await callback.message.delete()
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=text,
        reply_markup=kb
    )


@admin_router.callback_query(F.data.startswith('admin:accept_proofs:'))
async def check_proof(callback: types.CallbackQuery, bot, state: FSMContext):
    proof_id = int(callback.data.split(':')[-1])

    await proofs_client.accept_proof(proof_id)

    await callback.answer('✅ Подтверждено', show_alert=True)

    return await paginate_proof(callback, bot, state)


@admin_router.callback_query(F.data.startswith('admin:reject_proofs:'))
async def check_proof(callback: types.CallbackQuery, bot, state: FSMContext):
    proof_id = int(callback.data.split(':')[-1])

    await proofs_client.decline_proof(proof_id)

    await callback.answer('❌ Отклонено', show_alert=True)

    return await paginate_proof(callback, bot, state)


@admin_router.callback_query(F.data.startswith('admin:confirm_stop_activity:'))
@admin_router.callback_query(F.data.startswith('admin:stop_activity:'))
async def stop_activity(callback: types.CallbackQuery, state: FSMContext):
    activity_id = int(callback.data.split(':')[-1])

    if 'confirm_stop_activity' in callback.data:
        await activity_client.stop_activity(activity_id)
        await callback.answer('✅ Активность остановлена', show_alert=True)

        return await view_activity(callback, state)

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='❌ Отменить',
                    callback_data=f'admin:view_activity'
                ),
                types.InlineKeyboardButton(
                    text='✅ Остановить',
                    callback_data=f'admin:confirm_stop_activity:{activity_id}'
                ),
            ]
        ],
    )
    text = 'Вы уверены, что хотите остановить активность?'

    await callback.message.edit_text(
        text=text,
        reply_markup=kb
    )


@admin_router.callback_query(F.data.startswith('admin:activity_run:'))
async def start_activity(callback: types.CallbackQuery, state: FSMContext):
    activity_id = int(callback.data.split(':')[-1])

    await activity_client.run_activity(activity_id)

    await callback.message.edit_text(
        '✅ Активность запущена',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='✅ Ок',
                        callback_data=f'admin:view_activity'
                    ),
                ]
            ]
        )
    )
