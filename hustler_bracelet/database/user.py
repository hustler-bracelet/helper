# -*- coding: utf-8 -*-

from peewee import *
from hustler_bracelet.database.engine import database_engine


class User(Model):
    telegram_id = BigIntegerField(primary_key=True, unique=True, null=False)
    telegram_name = TextField(null=False)
    user_data_json = TextField(null=False)

    class Meta:
        database = database_engine
