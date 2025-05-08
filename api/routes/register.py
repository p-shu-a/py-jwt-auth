from fastapi import HTTPException, APIRouter, Depends
from api.db.database import get_db_session
from api.models.user import DBUser, UserIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt

api_router = APIRouter()

@api_router.post("/register", status_code=201)
async def register_handler(user: UserIn, session: AsyncSession = Depends(get_db_session)):

    query = select(DBUser).where(DBUser.username == user.username)
    result = await session.execute(query)
    user_exist = result.scalar_one_or_none()

    if user_exist:
        raise HTTPException(status_code=401, detail="user already registerd")
    
    db_user = DBUser(
        username=user.username,
        password= bcrypt.hashpw(str.encode(user.password), bcrypt.gensalt(10)).decode(),
    )
    
    session.add(db_user)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"failed to register user {e}")
    
    return {"message": f"{user.username} registerd successfully"}




# define a /router/{username} end point to tell user they are registered or not
# move as much of the path operations as possible into the api_router declaration
# look more into path operators in fastapi
# and dependiencies too
# what are tags? just for documentation?