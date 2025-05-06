from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from api.core.token import require_valid_token

api_router = APIRouter()

# can i define a custom decorator which mandates that a jwt be present?
# YES WE CAN! and we can validate the token in the deco too!
@api_router.get("/secret", status_code=201)
@require_valid_token
async def secret_hander(request: Request):
    return FileResponse("static/hamster_dance.gif", media_type="image/gif")  