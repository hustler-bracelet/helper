# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass, asdict
from hustler_bracelet.calendar.calendar_event import CalendarEvent


@dataclass
class UserData:
    income_categories: list[str]
    spending_categories: list[str]
    calendar_events: list[CalendarEvent]

    @classmethod
    def create_empty(cls) -> UserData:
        return UserData(
            income_categories=[],
            spending_categories=[],
            calendar_events=[]
        )

    def get_dict(self) -> dict:
        return asdict(self)
