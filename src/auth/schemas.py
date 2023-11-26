import datetime

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    registration_at: datetime.datetime
    role_id: int
    pass


class UserCreate(schemas.BaseUserCreate):
    id: int
    username: str
    registration_at: datetime.datetime
    role_id: int
    pass


'''class UserUpdate(schemas.BaseUserUpdate):
    pass'''