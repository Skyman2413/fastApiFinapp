from typing import Optional
from typing_extensions import override

from config import SECRET

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models

from auth.models import User
from auth.utils import get_user_db, SQLAlchemyUserDatabaseExtended


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    user_db: SQLAlchemyUserDatabaseExtended

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    '''async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")'''

    async def get_by_username(self, username) -> models.UP:
        """
                Get a user by username.

                :param username: E-mail of the user to retrieve.
                :raises UserNotExists: The user does not exist.
                :return: A user.
                """
        user = await self.user_db.get_by_username(username)

        if user is None:
            raise exceptions.UserNotExists()

        return user

    @override
    async def authenticate(
            self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:
        """
        Authenticate and return a user following a username/email and a password.

        Will automatically upgrade password hash if necessary.

        :param credentials: The user credentials.
        """
        try:
            user = await self.get_by_username(credentials.username)
        except exceptions.UserNotExists:
            user = await self.get_by_email(credentials.username)
        except exceptions.UserNotExists:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
