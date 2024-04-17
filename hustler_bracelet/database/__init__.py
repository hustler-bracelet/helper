# -*- coding: utf-8 -*-

from .user import UserTable, UserData
from .category import CategoryType, CategoryTable
from .event import EventTable

UserTable.create_table(safe=True)
CategoryTable.create_table(safe=True)
EventTable.create_table(safe=True)
