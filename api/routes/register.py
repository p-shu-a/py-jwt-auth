from fastapi import HTTPException, APIRouter, Depends
from api.db.database import get_db_session
from api.models.user import DBUser, UserIn, RegisterUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

api_router = APIRouter()

@api_router.post("/register", status_code=201)
async def register_handler(user: UserIn, session: AsyncSession = Depends(get_db_session)):

    query = select(DBUser).where(DBUser.username == user.username)
    result = await session.execute(query)
    user_exist = result.scalar_one_or_none()

    if user_exist:
        raise HTTPException(status_code=401, detail="user already registerd")
    
    reg_user = RegisterUser(user.username, user.password, "internet", "127.0.0.1")

    db_user = DBUser(
        username=reg_user.username,
        password=reg_user.password.decode(),
        location=reg_user.location,
        ip_addr=reg_user.ip_addr,
        created_at=reg_user.created_at
    )

    session.add(db_user)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"failed to register user {e}")
    
    return {"message": f"{user.username} registerd successfully"}

