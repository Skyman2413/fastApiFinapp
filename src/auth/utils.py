from fastapi import Depends

from database import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User, SQLAlchemyUserDatabaseExtended


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabaseExtended(session, User)
