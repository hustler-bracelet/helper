from peewee import *

from hustler_bracelet.database import UserTable
from hustler_bracelet.database.engine import database_engine
from hustler_bracelet.enums import CategoryType


class CategoryTable(Model):
    id = BigIntegerField(primary_key=True, unique=True, null=False)
    name = TextField(null=False)
    category_type: CategoryType = TextField(null=False)
    user = ForeignKeyField(UserTable, backref='categories', null=False)

    class Meta:
        database = database_engine
