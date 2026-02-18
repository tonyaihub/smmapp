from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from ..database import User, async_session
from ..models import User
from fastapi import Depends

SECRET = "SECRET"  # из .env

cookie_transport = CookieTransport(cookie_max_age=3600*24*30, cookie_secure=True)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600*24*30)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

user_db = SQLAlchemyUserDatabase(User, async_session)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,  # нужно реализовать или взять из fastapi-users примеров
    [auth_backend],
)

router = fastapi_users.get_auth_router(auth_backend)
router.include_router(fastapi_users.get_register_router(), prefix="/register")
router.include_router(fastapi_users.get_reset_password_router(), prefix="/forgot-password")
# и т.д.
