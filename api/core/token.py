from functools import wraps
from fastapi import HTTPException, Request
from api.core.globals import SECRET_KEY, HASH_ALGO, master_user_db
import jwt
import time


# here we define a custom decorator which can be applied to all functions/handlers that we want to require a JWT to execute
def require_valid_token(handler_func):
    @wraps(handler_func)
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


def generate_jwt(username):
    payload = {
        "username": username,
        "iss": "SCDP",
        "exp": int(time.time()) + 900 # 15mins * 60secs
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=HASH_ALGO)
    return token