# -*- coding: utf-8 -*-

from hustler_bracelet.database.user import User
from hustler_bracelet.database.user_data import UserData


class Database:
    def __init__(self, telegram_id: int) -> None:
        self._telegram_id = telegram_id
        User.Meta.database.connect(reuse_if_open=True)
        User.create_table(safe=True)

    def do_i_exist(self) -> bool:
        return User.get(User.telegram_id == self._telegram_id) is None

    def create_me(self, telegram_name: str) -> User:
        new_user = User(
            telegram_id=self._telegram_id,
            telegram_name=telegram_name,
            user_data=UserData.create_empty()
        )
        new_user.save(force_insert=True)
        return new_user
