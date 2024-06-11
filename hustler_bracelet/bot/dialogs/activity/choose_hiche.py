import operator
from uuid import uuid1

from aiogram import F, types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common.items import ItemsGetterVariant
from aiogram_dialog.widgets.kbd import Radio, Column, Cancel, Row, Button
from aiogram_dialog.widgets.text import Format, Const, Jinja

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.client import NichesAPIClient, ActivityAPIClient
from hustler_bracelet.client.schemas import ActivityDataResponse


niche_client = NichesAPIClient()


async def niches_texts_getter(dialog_manager: DialogManager, **kwargs):
    activity: ActivityDataResponse = dialog_manager.start_data.get('activity')

    if activity is None:
        raise ValueError('Не удалось получить данные об активности')

    radio_widget: Radio = dialog_manager.find('r_activities')

    activity_caption = activity.niches[0].name if activity.niches else None
    checked_item_id = radio_widget.get_checked()
    for caption_item_id, caption_ in [
        (data.id, data.name)
        for data in activity.niches
    ]:
        if checked_item_id == caption_item_id:
            activity_caption = caption_
            break

    activity_name_mapping = {
        data.id: data.name
        for data in activity.niches
    }
    activity_emojy_mapping = {
        data.id: data.emoji
        for data in activity.niches
    }

    if (activity_caption is None) and (checked_item_id is not None):
        raise ValueError(f'Описание для элемента {checked_item_id} не найдено')

    return {
        'activity_emojy': activity_emojy_mapping.get(checked_item_id),
        'activity_name': activity_name_mapping.get(checked_item_id),
        'activity_caption': activity_caption,
    }


async def activity_getter(dialog_manager: DialogManager, **kwargs):
    activity: ActivityDataResponse = dialog_manager.start_data.get('activity')
    return {
        'activity_emojy': activity.emoji,
        'activity_name': activity.name,
        'activity_caption': activity.description,
        'activity_reward': activity.fund,
        'total_places': activity.total_places,
    }


def niches_getter(data: dict):
    activity: ActivityDataResponse = data['start_data']['activity']

    if activity is None:
        raise ValueError('Не удалось получить данные об активности')

    return [
        (data.id, data.name)
        for data in activity.niches
    ]


async def on_choose_hiche_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager
):
    radio_widget: Radio = manager.find('r_activities')
    checked_item_id = radio_widget.get_checked()
    if checked_item_id is None:
        await callback.answer('Выбери категорию!')
        return

    await niche_client.select_niche_by_id(
        user_id=callback.from_user.id,
        niche_id=checked_item_id
    )

    await manager.next()


async def on_click_go_tasks(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager
):
    activity: ActivityDataResponse = manager.start_data.get('activity')

    activity_summary = await ActivityAPIClient().get_activity_user_summary(
        user_id=callback.from_user.id,
        activity_id=activity.id
    )

    await manager.start(
        states.ActivityTask.MAIN,
        data={'activity_summary': activity_summary}
    )


choose_niche_dialog = Dialog(
    Window(
        Jinja(
            '💰 <b>Сезон крипты</b>\n'
            '\n'
            'Ну что, хаслеры, время пампить, дампить, хуямпить, МММ’ить, и регулировать стаканы!\n'
            'Выбирай свою нишу и вперёд жарить стейкинги!\n'
            '\n'
            'Во время активности ты сможешь получать задания, выполнять их и получать за это баллы, продвигаясь в топе.\n'
            '\n'
            'Чем выше ты в топе, тем больше кусок тебе перепадёт из призового фонда в <b>{{activity_reward|money}}</b>!\n'
            'И даже если ты оказался на самом последнем месте, <b>денежный приз ты всё равно получишь!</b>\n'
            'Поторопись, осталось всего лишь 16 мест...\n'  # TODO: А оно нам надо?
            '\n'
            'Но для начала...\n'
            '<b>Выбери нишу, в которой ты работаешь</b> 👇',
            when=~F['activity_caption']
        ),
        Format(
            '{activity_emojy} <b>{activity_name}</b>\n'
            '\n'
            '<i>{activity_caption}</i>\n'
            '\n'
            '👉 <b>Выбираешь эту нишу?</b>',
            when=F['activity_caption']
        ),
        Column(
            Radio(
                Format("[{item[1]}]"),
                Format("{item[1]}"),
                id="r_activities",
                item_id_getter=operator.itemgetter(0),
                items=niches_getter
            )
        ),
        Row(
            Cancel(Const('❌ Отмена')),
            Button(
                Const('✅ Выбрать'),
                id='choose_activity',
                on_click=on_choose_hiche_click
            ),
        ),
        state=states.ActivityOnboarding.MAIN
    ),
    Window(
        Jinja(
            '💰 <b>{{activity_name}}</b>\n'
            '\n'
            '🎉 <b>Добро пожаловать в активность, {{activity_name}}!</b>\n'
            'Тебе и ещё <b>{{total_places - 1}}</b> предстоит побороться за\n'
            '<b>{{activity_reward|money}}</b>, как можно быстрее выполняя задания, набирая баллы и пробиваясь в топ!\n'
            '\n'
            '⚡️ А вот и первое задание подъехало. Погнали?'
        ),
        Button(
            Const('➡️ Перейти к заданию'), 
            id='go_tasks_activity',
            on_click=on_click_go_tasks,
        ),
        state=states.ActivityOnboarding.FINAL
    ),
    getter=(niches_texts_getter, activity_getter)
)
