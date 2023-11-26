from fastapi import FastAPI

import tasks.router
from auth.auth import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate, UserUpdate


app = FastAPI(
    title="Банка счастья",
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/bearer",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    router=tasks.router.router,
    prefix="/test_mail",
    tags=["mail"]
)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

