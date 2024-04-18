import json
from dataclasses import dataclass
from datetime import date

from hustler_bracelet.controllers.event import Event
from hustler_bracelet.database import UserTable, CategoryTable


@dataclass
class User:
    id: int
    tg_name: str
    user_data: dict | str
    balance: float

    _db_instance: UserTable | None = None

    def __post_init__(self):
        if isinstance(self.user_data, str):
            self.user_data = json.loads(self.user_data)

        try:
            self._db_instance = self._db_instance or UserTable.get_by_id(self.id)
        except:
            self._db_instance = UserTable(
                telegram_id=self.id,
                telegram_name=self.tg_name,
                user_data_json=json.dumps(self.user_data),
                balance=self.balance
            )
            self._db_instance.save(force_insert=True)

    def save(self):
        self._db_instance.telegram_name = self.tg_name
        self._db_instance.user_data_json = json.dumps(self.user_data)
        self._db_instance.balance = self.balance

        self._db_instance.save(force_insert=True)

    @classmethod
    def get_by_id(cls, id_: int):
        db_instance = UserTable.get_by_id(id_)
        return cls.from_db_instance(db_instance=db_instance)

    @classmethod
    def from_db_instance(cls, db_instance: UserTable):
        return cls(
            id=db_instance.telegram_id,
            tg_name=db_instance.telegram_name,
            user_data=json.loads(db_instance.user_data_json),
            balance=db_instance.balance,
            _db_instance=db_instance
        )

    def delete(self):
        self._db_instance.delete_instance()

    def iter_events(self, limit: int | None = None):
        query = self._db_instance.events
        if limit is not None:
            query = query.limit(limit)

        from hustler_bracelet.controllers.event import Event
        yield from (Event.get_by_id(db_event.id) for db_event in query)
    
    def iter_events_filtered_by_date(self, min_date: date, max_date: date | None = None, limit: int | None = None):
        max_date = max_date or min_date

        for event in self.iter_events(limit=limit):
            if min_date >= event.timestamp.date() >= max_date:
                yield event
    
    def get_events_list(self, limit: int | None = None) -> list[Event]:
        return [*self.iter_events(limit=limit)]
    
    def get_events_list_filtered_by_date(self, min_date: date, max_date: date | None = None, limit: int | None = None) -> list[Event]:
        return [*self.iter_events_filtered_by_date(min_date=min_date, max_date=max_date, limit=limit)]

    def iter_categories(self, limit: int | None = None):
        query = CategoryTable.select().where(CategoryTable.user == self._db_instance)

        if limit is not None:
            query = query.limit(limit)

        from hustler_bracelet.controllers.category import Category
        yield from (Category.from_db_instance(db_category) for db_category in query)

    def get_categories_list(self, limit: int | None = None) -> list['Category']:
        return [*self.iter_categories(limit=limit)]
