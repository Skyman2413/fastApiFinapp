from typing import Optional

from fastapi import Depends
from fastapi_users.db import BaseUserDatabase
from fastapi_users.models import UP
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabaseExtended(session, User)


class SQLAlchemyUserDatabaseExtended(SQLAlchemyUserDatabase):
    async def get_by_username(self, username: str) -> Optional[UP]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.username) == func.lower(username)
        )
        return await self._get_user(statement)
