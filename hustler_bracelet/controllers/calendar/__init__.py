# -*- coding: utf-8 -*-

from datetime import date
from hustler_bracelet.controllers.calendar.calendar_event import CalendarEvent
from hustler_bracelet.database import User


class Calendar:
    def __init__(self, user: User):
        user.do_i_exist()

    def get_events(self, day: date | None) -> list[CalendarEvent]:
        raise NotImplementedError

    def get_event_history(self) -> list[CalendarEvent]:
        raise NotImplementedError
