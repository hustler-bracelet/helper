from enum import Enum

from peewee import *

from hustler_bracelet.database import UserTable
from hustler_bracelet.database.engine import database_engine


class CategoryType(str, Enum):
    income = 'income'
    spend = 'spend'


class CategoryTable(Model):
    id = BigIntegerField(primary_key=True, unique=True, null=False)
    name = TextField(null=False)
    category_type: CategoryType = TextField(null=False)
    user = ForeignKeyField(UserTable, backref='categories', null=False)

    class Meta:
        database = database_engine
