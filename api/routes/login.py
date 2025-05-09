from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.models.user import DBUser, UserIn
from api.core.token import generate_jwt
from api.db.database import get_db_session

import bcrypt

api_router = APIRouter()

@api_router.post("/login", status_code=201)
async def login_handler(login_user: UserIn, session: AsyncSession = Depends(get_db_session)):

    query = select(DBUser).where(login_user.username == DBUser.username)
    result = await session.execute(query)
    saved_user = result.scalar_one_or_none()

    if saved_user is None:
        raise HTTPException(404, f"{login_user.username} not found. register first")
    else:
        print(type(saved_user))
        if bcrypt.checkpw(str.encode(login_user.password), saved_user.password.encode()):
            token = generate_jwt(saved_user.username)
            ret_resp = {"success": f"{login_user.username} logged in",
                        "auth_token": token}
            return ret_resp
        else:
            raise HTTPException(401, "invalid password")