from _datetime import datetime
from typing import Optional

from fastapi_users.models import UP
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import MetaData, Table, Column, Integer, String, JSON, TIMESTAMP, ForeignKey, Boolean, func, select

from database import Base

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON)
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("email", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registration_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=True, nullable=False),
    Column("is_verified", Boolean, default=True, nullable=False),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    """ from source
            id: ID
            email: str
            hashed_password: str
            is_active: bool
            is_superuser: bool
            is_verified: bool
    """
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    registration_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(role.c.id))


class SQLAlchemyUserDatabaseExtended(SQLAlchemyUserDatabase):
    async def get_by_username(self, username: str) -> Optional[UP]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.username) == func.lower(username)
        )
        return await self._get_user(statement)
