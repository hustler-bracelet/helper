from aiogram.fsm.state import State, StatesGroup


class Scrolls(StatesGroup):
    MAIN = State()
    DEFAULT_PAGER = State()
    PAGERS = State()
    LIST = State()
    TEXT = State()
    STUB = State()
    SYNC = State()


class Main(StatesGroup):
    MAIN = State()


class Layouts(StatesGroup):
    MAIN = State()
    ROW = State()
    COLUMN = State()
    GROUP = State()


class Selects(StatesGroup):
    MAIN = State()
    SELECT = State()
    RADIO = State()
    MULTI = State()
    TOGGLE = State()


class Calendar(StatesGroup):
    MAIN = State()
    DEFAULT = State()
    CUSTOM = State()


class FinanceMainMenu(StatesGroup):
    MAIN = State()


class FinanceCategoriesManagementMenu(StatesGroup):
    MAIN = State()


class FinanceInvestmentsMenu(StatesGroup):
    MAIN = State()


class AddFinanceEvent(StatesGroup):
    MAIN = State()
    ENTER_VALUE = State()
    CHOOSE_DATE = State()
    FINAL = State()


class AddFinanceCategory(StatesGroup):
    MAIN = State()
    ENTER_NAME = State()
    FINAL = State()


class DeleteFinanceCategory(StatesGroup):
    MAIN = State()


class Planning(StatesGroup):
    MAIN = State()


class AddTask(StatesGroup):
    MAIN = State()
    GET_DATE = State()
    FINAL = State()


class CompleteSomeTasks(StatesGroup):
    MAIN = State()


class Sport(StatesGroup):
    MAIN = State()


class SettingsMainMenu(StatesGroup):
    MAIN = State()


class ChangeCurrencySetting(StatesGroup):
    MAIN = State()


class AboutBot(StatesGroup):
    MAIN = State()


class EraseAllDataAboutUser(StatesGroup):
    MAIN = State()


class Counter(StatesGroup):
    MAIN = State()


class Multiwidget(StatesGroup):
    MAIN = State()


class ReplyKeyboard(StatesGroup):
    MAIN = State()


class Switch(StatesGroup):
    MAIN = State()
    INPUT = State()
    LAST = State()
