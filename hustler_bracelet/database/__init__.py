# -*- coding: utf-8 -*-

from .user import UserTable, UserData
from .category import CategoryType, CategoryTable
from .events import EventTable

if __name__ == '__main__':
    user = UserTable(
        telegram_id=0,
        telegram_name='Hulio',
        user_data_json='{}'
    )
    user.create()
    UserTable
