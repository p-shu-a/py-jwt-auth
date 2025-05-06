from fastapi import HTTPException, APIRouter
from api.models.user import UserIn
from api.core.globals import master_user_db
from api.core.token import generate_jwt
import bcrypt

api_router = APIRouter()

@api_router.post("/login", status_code=201)
async def login_handler(login_user: UserIn):
    if login_user.username not in master_user_db:
        raise HTTPException(404, f"{login_user.username} not found. register first")
    else:
        saved_user = master_user_db[login_user.username]
        print(type(saved_user))
        if bcrypt.checkpw(str.encode(login_user.password), saved_user.password):
            token = generate_jwt(saved_user.username)
            ret_resp = {"success": f"{login_user.username} logged in",
                        "auth_token": token}
            return ret_resp
        else:
            raise HTTPException(401, "invalid password")