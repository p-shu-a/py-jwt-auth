from fastapi.testclient import TestClient
import pytest_asyncio
from api.models.user import RegisterUser
from api.app import api
import time
import pytest
from httpx import ASGITransport, AsyncClient

print(AsyncClient)

client = TestClient(api)

TEST_USER_RESUABLE = RegisterUser("joan_holloway",
                                  "office_space",
                                  "internet",
                                  "127.0.0.1")

TEST_USER_RESUABLE_JSON = {"username": "joan_holloway",
                           "password": "office_space"}

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=api)
    async with AsyncClient(transport=transport, base_url="http://jwt_test") as client:
        yield client


# test saving a new user
@pytest.mark.asyncio
async def test_register_new_user(async_client):
    payload = {"username":f"joan_holloway_{int(time.time())}", "password":"office_space"}
    resp = await async_client.post("/register", json=payload)
    assert resp.status_code == 201
    assert resp.json() == {"message" : f"{payload['username']} registerd successfully"}

# Test saving an existing user.
@pytest.mark.asyncio
async def test_register_existing_user(async_client):
    resp = await async_client.post("/register", json=TEST_USER_RESUABLE_JSON)
    assert resp.status_code == 401
    assert resp.json() == {"detail": "user already registerd"}

# what if the user sending in junk json?
# we'll pydantic does most of the heavy lifting.
# its expecting a particular set of keys
# when the expected keys don't come it, it responds with a 422 and a wackass body...
@pytest.mark.asyncio
async def test_register_user_bad_json(async_client):
    payload = {"usernam": "foo_bar",
               "pa55w0rd": "bar_foo"}
    
    resp = await async_client.post("/register", json=payload)
    assert resp.status_code == 422

# try to log in as some non-existing user
@pytest.mark.asyncio
async def test_login_non_exist(async_client):
    payload = {"username":"john_cena",
               "password":"you_cant_see_mee"}
    resp = await async_client.post("/login", json=payload)
    assert resp.status_code == 404
    assert resp.json() == {"detail":f"{payload['username']} not found. register first"}

# test logging in with an existing user
@pytest.mark.asyncio
async def test_login_existing_user(async_client):
    
    resp = await async_client.post("/login", json=TEST_USER_RESUABLE_JSON)
    assert resp.status_code == 201
    resp_body = resp.json()
    assert "auth_token" in resp_body
    assert resp_body['success'] == f"{TEST_USER_RESUABLE_JSON['username']} logged in"

# user exists but password is incorrect
@pytest.mark.asyncio
async def test_existing_user_wrong_password(async_client):

    payload = {"username":TEST_USER_RESUABLE_JSON['username'],
               "password": "peggy_sue"}
    resp = await async_client.post("/login", json=payload)
    assert resp.status_code == 401
    assert resp.json()['detail'] == "invalid password"
