from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Next, Row, Back, Start
from aiogram_dialog.widgets.text import Const

from hustler_bracelet.bot.dialogs import states

onboarding_dialog = Dialog(
    Window(
        Const(
            '\n'
            '👋🏻 <b>Welcome aboard, hustler!</b>\n'
            '\n'
            'Туда-сюда-миллионер уже не катит. Этот бот внесет осознанность и систему в твои движения.\n'
            '\n'
            'Самый простой способ планировать свои задачи и управлять своими финансами уже у тебя на пальцах — потому что ты в HUSTLER BRACELET!\n'
            '\n'
            'Поворкаем?'
        ),
        Next(Const('Далее ➡️')),
        state=states.OnBoarding.MAIN
    ),
    Window(
        Const(
            '💸 <b>Финансы</b> \n'
            '\n'
            'Начнём с управления своим капиталом.\n'
            'Ты можешь регистрировать свои доходы и расходы, а также добавлять свои активы.\n'
            'Бот сам посчитает твой капитал, самые популярные категории доходов и трат, а также доходность по активам.\n'
            '\n'
            '📁 <b>Категории</b>\n'
            '\n'
            'У доходов и расходов есть свои категории. Например, у доходов могут быть категории «ворк по телеге» и «посредничество», а у расходов — «базовые потребности», «расходники» и «вуш самокатики мои любимые вуш самокатики».\n'
            'А бот посчитает твои самые прибыльные категории доходов и в каких категориях расходов тебе не стоит транжирить свой честно нахасленный кэш.\n'
            '\n'
            '📈 <b>Инвестиции</b> (бета)\n'
            '\n'
            'Ты можешь добавить свой актив с годовым процентом, и бот каждый месяц будет прибавлять к твоему капиталу доход по сложному проценту.\n'
            'Либо ты можешь не указывать процент и добавлять прибыль вручную.'
        ),
        Row(
            Back(Const('⬅️ Назад')),
            Next(Const('Далее ➡️'))
        ),
        state=states.OnBoarding.FINANCE
    ),
    Window(
        Const(
            '🕐  <b>Планирование</b>\n'
            '\n'
            'В этом боте ты также можешь управлять своими задачами, чтобы эффективнее добиваться своих целей и держать всё под контролем.\n'
            '\n'
            '📝  <b>Добавление задач</b>\n'
            '\n'
            'Быстро добавить задачу можно с главного экрана бота: для этого  нажми соответствующую кнопку.\n'
            'Введи название самой задачи и поставь дату, к которой задача должна быть выполнена.\n'
            'Вот и всё!\n'
            '\n'
            '✅ <b>Выполнение задач</b>\n'
            '\n'
            'Чтобы выполнить сделанные задачи, просто выбери соответствующую кнопку в меню планирования, нажми на задачи, которые хочешь выполнить, и нажми на кнопку Выполнить.\n'
            'Выполненные задачи убираются из списка.\n'
            '\n'
            '📊 <b>Статистика</b>\n'
            '\n'
            'В меню планирования отображается количество выполненных за всё время задач.'
        ),
        Row(
            Back(Const('⬅️ Назад')),
            Next(Const('Далее ➡️'))
        ),
        state=states.OnBoarding.PLANNING
    ),
    Window(
        Const(
            '💪 <b>Спорт</b>\n'
            '\n'
            'Уже в мае ты сможешь апнуть свою игру здорового образа жизни:\n'
            ' • Расчёт КБЖУ по названию блюда\n'
            ' • Трекинг калорий и питания\n'
            ' • Трекинг тренировок\n'
            ' • Статистика\n'
            ' • Советы от квалифицированного тренера (потому что ты в браслете 😉)\n'
            'и многое другое...'
        ),
        Row(
            Back(Const('⬅️ Назад')),
            Next(Const('Далее ➡️'))
        ),
        state=states.OnBoarding.SPORT
    ),
    Window(
        Const(
            'На самом деле, бот довольно-таки интуитивно понятный.\n'
            '\n'
            'Но если возникнут вопросы - пиши @ambienthugg или кодеру @d_nsdkin.\n'
            '\n'
            'Удачи! 👋'
        ),
        Row(
            Back(Const('⬅️ Назад')),
            Start(
                Const('Перейти в бота ➡️'),
                id='main_menu',
                state=states.Main.MAIN,
                mode=StartMode.RESET_STACK
            )
        ),
        state=states.OnBoarding.FINAL
    ),
)
