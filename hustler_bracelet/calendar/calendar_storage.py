# -*- coding: utf-8 -*-

from datetime import date, time, datetime
from hustler_bracelet.calendar.calendar_event import CalendarEvent


class CalendarStorage:
    def get_events_for_day(self, day: date) -> list[CalendarEvent]:
        ...

    def add_event(self, event: CalendarEvent) -> None:
        ...
