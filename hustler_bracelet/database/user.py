from __future__ import annotations

from dataclasses import asdict, dataclass

from peewee import *
from hustler_bracelet.database.engine import database_engine


@dataclass
class UserData:
    income_categories: list[int]
    spending_categories: list[int]

    @classmethod
    def create_empty(cls) -> UserData:
        return UserData(
            income_categories=[],
            spending_categories=[]
        )

    def get_dict(self) -> dict:
        return asdict(self)


class UserTable(Model):
    telegram_id = BigIntegerField(primary_key=True, unique=True, null=False)
    telegram_name = TextField(null=False)
    user_data_json = TextField(null=False)
    balance = FloatField(null=False, default=0.)

    class Meta:
        database = database_engine


if __name__ == '__main__':
    user_data = UserData([1, 2, 3], [3, 2, 1])
    print(user_data)
    print(user_data.get_dict())
    print(UserData(**user_data.get_dict()))

# [{'event_time': datetime.datetime(2024, 4, 16, 23, 22, 3, 85571)}]
# [CalendarEvent(event_time=datetime.datetime(2024, 4, 16, 23, 22, 3, 85571))]
