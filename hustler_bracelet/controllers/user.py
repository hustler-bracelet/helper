from datetime import datetime, date

from hustler_bracelet.controllers.event import Event
from hustler_bracelet.database import UserData, UserTable


class User:
    def __init__(self, telegram_id: int, notexists_ok: bool = False) -> None:
        self._telegram_id = telegram_id

        UserTable.Meta.database.connect(reuse_if_open=True)
        UserTable.create_table(safe=True)

        if (not self.do_i_exist()) and not notexists_ok:
            raise ValueError(f'User with {telegram_id=} not found')

    def do_i_exist(self) -> bool:
        return UserTable.get(UserTable.telegram_id == self._telegram_id) is not None

    def create_me(self, telegram_name: str) -> UserTable:
        new_user = UserTable(
            telegram_id=self._telegram_id,
            telegram_name=telegram_name,
            user_data=UserData.create_empty()
        )
        new_user.save(force_insert=True)

        return new_user

    def get_events_list_by_date(self, min_date: date, max_date: date | None = None, limit: int | None = None) -> list[Event]:
        pass

    def get_events_list(self) -> list[Event]:
        pass

    def add_event(self, event: Event, date_and_time: datetime | None = None):
        date_and_time = date_and_time or datetime.now()

        pass

    def remove_event(self, event: Event):
        pass
