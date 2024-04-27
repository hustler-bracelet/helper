import operator

from aiogram_dialog.widgets.kbd import Button, Row, Select
from aiogram_dialog.widgets.kbd.select import OnItemClick
from aiogram_dialog.widgets.text import Const, Format


def get_choose_category_type_kb(on_category_type_selected: OnItemClick, category_name_suffix: str = 'ы'):
    return Select(
        Format('{item[0]}'),
        id='slct_category_type',
        item_id_getter=operator.itemgetter(1),
        items=(
            (f'Доход{category_name_suffix}', 'income'),
            (f'Расход{category_name_suffix}', 'spending'),
        ),
        on_click=on_category_type_selected,
    )
