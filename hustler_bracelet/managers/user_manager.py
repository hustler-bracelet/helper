# -*- coding: utf-8 -*-

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from hustler_bracelet.database.user import User


class UserManager:
    def __init__(self, telegram_id: int, session: AsyncSession) -> None:
        self._telegram_id = telegram_id
        self._session = session

    @property
    def telegram_id(self):
        return self._telegram_id

    def get_database_session(self) -> AsyncSession:
        return self._session

    async def _is_user_exists(self):
        query_result = (
            await self._session.exec(
                select(User)
                .where(
                    User.telegram_id == self._telegram_id
                )
            )
        ).all()
        return bool(query_result)

    async def create_new_user(self, telegram_name: str):
        assert not await self._is_user_exists()

        new_user = User(
            telegram_id=self._telegram_id,
            telegram_name=telegram_name,
            current_balance=0.0
        )
        self._session.add(new_user)
        await self._session.commit()

        return new_user

    async def create_user_if_not_exists(self, telegram_name: str) -> bool:
        create_new_user = not await self._is_user_exists()

        if create_new_user:
            await self.create_new_user(telegram_name)

        return create_new_user

    async def __aenter__(self):
        return await self._session.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._session.__aexit__(exc_type, exc_val, exc_tb)
