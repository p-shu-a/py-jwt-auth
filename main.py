from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
import bcrypt
import time
import jwt
import functools

api = FastAPI()

master_user_db = dict()
SECRET_KEY = "taen$ighee0iegh2si3Usie"
HASH_ALGO = "HS256"

class RegisterUser:
    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt(10))
    
    def __repr__(self):
        return str({
            "username": self.username,
            "password": self.password
        })
    
class UserIn(BaseModel):
    username: str
    password: str


@api.get("/health")
def health_check():
    return {"status": "The wizards have landed...status okay"}


@api.post("/register", status_code=201)
async def register_handler(user: UserIn):
    if user.username in master_user_db:
        raise HTTPException(401, "user already registerd")
    
    user = RegisterUser(user.username, user.password)
    master_user_db[user.username] = user

    return {"message": f"{user.username} registerd successfully"}

def generate_jwt(username):
    payload = {
        "username": username,
        "iss": "SCDP",
        "exp": int(time.time()) + 900 # 15mins * 60secs
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=HASH_ALGO)
    return token


@api.post("/login", status_code=201)
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


# here we define a custom decorator which can be applied to all functions/handlers that we want to require a JWT to execute
def require_valid_token(handler_func):
    @functools.wraps(handler_func)
    async def wrapper(**kwargs):             # notice how the wrapper needs to be async...if the func its wrapping is async, the wrapper need to be async
        request: Request = kwargs.get("request")
        if request is None:
            raise HTTPException(500, detail="Corrupt or non-existant Request")
        
        auth_header = request.headers.get("authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(401, detail="Invalid or missing token")
        token = auth_header.split(" ")[1] # get just the token

        # try to decode the token, and catch possible exceptions...
        # not sure what the difference between invalid sig and invalid token is
        # if there is a sig error, can a token still be valid (or vice versa)?
        try:
            jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGO])
        except (jwt.InvalidSignatureError, jwt.InvalidTokenError) as e:
            raise HTTPException(401, detail="Invalid Token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, detail="Token Expired")
        return await handler_func(**kwargs)
    return wrapper


# can i define a custom decorator which mandates that a jwt be present?
# YES WE CAN! and we can validate the token in the deco too!
@api.get("/secret", status_code=201)
@require_valid_token
async def secret_hander(request: Request):
    return FileResponse("./hamster_dance.gif", media_type="image/gif")


'''
# running list of questions

- how does the execution compare to GO? An out-call is made to a goroutine and the parent function continues execution, and does not block, unless told to do so. is that the same here? yes, i think so. thats what the await keyword is doing. if you don't include it, execution carries on.
- 
'''