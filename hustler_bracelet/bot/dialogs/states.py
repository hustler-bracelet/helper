from aiogram.fsm.state import State, StatesGroup


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


class FinanceEventsListMenu(StatesGroup):
    MAIN = State()
    LIST = State()


class FinanceInvestmentsMenu(StatesGroup):
    MAIN = State()


class AddFinanceAsset(StatesGroup):
    MAIN = State()
    BASE_AMOUNT = State()
    INTEREST_RATE = State()
    FINAL = State()


class DeleteAssets(StatesGroup):
    MAIN = State()


class RenameAsset(StatesGroup):
    MAIN = State()
    ENTER_NAME = State()


class ChangeInterestRate(StatesGroup):
    MAIN = State()
    ENTER_INTEREST_RATE = State()


class AddInvestmentProfit(StatesGroup):
    MAIN = State()
    PROFIT = State()
    FINAL = State()


class AddFinanceEvent(StatesGroup):
    MAIN = State()
    ENTER_VALUE = State()
    CHOOSE_DATE = State()
    FINAL = State()


class AddFinanceCategory(StatesGroup):
    ENTER_NAME_FROM_EVENT_ADDING = State()
    MAIN = State()
    ENTER_NAME = State()
    FINAL = State()


class DeleteFinanceCategory(StatesGroup):
    MAIN = State()
    CHOOSE_CATEGORY = State()
    FINAL = State()


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
    FINAL = State()


class FixBalance(StatesGroup):
    MAIN = State()
    FINAL = State()


class OnBoarding(StatesGroup):
    MAIN = State()
    FINANCE = State()
    PLANNING = State()
    SPORT = State()
    FINAL = State()


class Activities(StatesGroup):
    MAIN = State()
