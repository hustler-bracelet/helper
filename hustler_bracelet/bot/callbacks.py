from aiogram.filters.callback_data import CallbackData


class CategoryForNewEventCallback(CallbackData, prefix='cat_fr_nw_evnt', sep='.'):
    category_id: int
