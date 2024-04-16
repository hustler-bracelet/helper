# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CalendarEvent:
    event_time: datetime
