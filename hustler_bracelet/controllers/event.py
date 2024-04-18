from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime

from hustler_bracelet.database import EventTable


@dataclass
class Event:
    id: int
    name: str
    value: float
    category: 'category.Category' | int

    timestamp: datetime | float

    data: dict | list | str

    _db_instance: EventTable | None = None

    def __post_init__(self):
        if isinstance(self.category, int):
            from hustler_bracelet.controllers.category import Category
            self.user = Category.get_by_id(self.category)

        if isinstance(self.timestamp, float):
            self.timestamp = datetime.fromtimestamp(self.timestamp)

        if isinstance(self.data, str):
            self.data = json.loads(self.data)

        try:
            self._db_instance = self._db_instance or EventTable.get_by_id(self.id)
        except:
            self._db_instance = EventTable(
                id=self.id,
                name=self.name,
                value=self.value,
                category=self.category.id,
                timestamp=self.timestamp,
                data=json.dumps(self.data)
            )
            self._db_instance.save(force_insert=True)

    def save(self):
        self._db_instance.name = self.name
        self._db_instance.value = self.value
        self._db_instance.category = self.category.id
        self._db_instance.timestamp = self.timestamp
        self._db_instance.data_json = json.dumps(self.data)

        self._db_instance.save(force_insert=True)

    @classmethod
    def get_by_id(cls, id_: int):
        db_instance = EventTable.get_by_id(id_)
        return cls.from_db_instance(db_instance=db_instance)

    @classmethod
    def from_db_instance(cls, db_instance: EventTable):
        return cls(
            id=db_instance.id,
            name=db_instance.name,
            value=db_instance.value,
            category=db_instance.category.id,
            timestamp=db_instance.timestamp,
            data=json.loads(db_instance.data_json),
            _db_instance=db_instance
        )
