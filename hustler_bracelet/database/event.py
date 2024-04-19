from peewee import *

from hustler_bracelet.database.category import CategoryTable
from hustler_bracelet.database.engine import database_engine


class EventTable(Model):
    id = BigIntegerField(primary_key=True, unique=True, null=False)
    name = TextField(null=False)
    value = FloatField(null=False)
    category = ForeignKeyField(CategoryTable, backref='events', null=False)

    date_ordinal = IntegerField(null=False)

    data_json = TextField(null=False, default='{}')

    class Meta:
        database = database_engine
