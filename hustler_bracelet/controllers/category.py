from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date

from hustler_bracelet.controllers.user import User
from hustler_bracelet.database import CategoryTable, EventTable
from hustler_bracelet.enums import CategoryType


@dataclass()
class Category:
    id: int
    name: str
    type: CategoryType | str
    user: User | int

    _db_instance: CategoryTable | None = None

    def __post_init__(self):
        if not isinstance(self.type, CategoryType):
            self.type = CategoryType(self.type)

        if isinstance(self.user, int):
            self.user = User(self.user)

        try:
            self._db_instance = self._db_instance or CategoryTable.get_by_id(self.id)
        except:
            self._db_instance = CategoryTable(
                id=self.id,
                name=self.name,
                category_type=self.type,
                user=self.user.id
            )
            self._db_instance.save(force_insert=True)

    def save(self):
        self._db_instance.name = self.name
        self._db_instance.category_type = self.type
        self._db_instance.user = self.user.id

        self._db_instance.save(force_insert=True)

    @classmethod
    def get_by_id(cls, id_: int):
        db_instance = CategoryTable.get_by_id(id_)
        return cls.from_db_instance(db_instance=db_instance)

    @classmethod
    def from_db_instance(cls, db_instance: CategoryTable):
        return cls(
            id=db_instance.id,
            name=db_instance.name,
            type=db_instance.category_type,
            user=db_instance.user.id,
            _db_instance=db_instance
        )

    def delete(self):
        self._db_instance.delete_instance()

    def iter_events(self, limit: int | None = None):
        query = self._db_instance.events
        if limit is not None:
            query = query.limit(limit)

        from hustler_bracelet.controllers.event import Event
        yield from (Event.from_db_instance(db_event) for db_event in query)

    def iter_events_filtered_by_date(self, min_date: date, max_date: date | None = None, limit: int | None = None):
        max_date = max_date or min_date

        for event in self.iter_events(limit=limit):
            if min_date >= event.timestamp.date() >= max_date:
                yield event

    def get_events_list(self, limit: int | None = None):
        return [*self.iter_events(limit=limit)]

    def get_events_list_filtered_by_date(self, min_date: date, max_date: date | None = None, limit: int | None = None):
        return [*self.iter_events_filtered_by_date(min_date=min_date, max_date=max_date, limit=limit)]
