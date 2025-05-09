from api.models.user import RegisterUser
import time
import pytest

TEST_USER_RESUABLE = RegisterUser("joan_holloway",
                                  "office_space",
                                  "internet",
                                  "127.0.0.1")

def get_test_user():
    return {"username": f"joan_holloway_{int(time.time())}", "password": "office_space"}

# test saving a new user
@pytest.mark.asyncio
async def test_register_new_user(async_client):     # async_client is injected as a dependancy by pytest. its automagic
    payload = get_test_user()
    resp = await async_client.post("/register", json=payload)
    assert resp.status_code == 201
    assert resp.json() == {"message" : f"{payload['username']} registerd successfully"}

# Test saving an existing user.
@pytest.mark.asyncio
async def test_register_existing_user(async_client):
    payload = get_test_user()
    await async_client.post("/register", json=payload)
    resp = await async_client.post("/register", json=payload)
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
    payload = get_test_user()
    resp = await async_client.post("/login", json=payload)
    assert resp.status_code == 201
    resp_body = resp.json()
    assert "auth_token" in resp_body
    assert resp_body['success'] == f"{payload['username']} logged in"

# user exists but password is incorrect
@pytest.mark.asyncio
async def test_existing_user_wrong_password(async_client):

    payload = get_test_user()
    await async_client.post("/login",json=payload)
    payload = {"username":payload['username'],
               "password": "peggy_sue"}
    resp = await async_client.post("/login", json=payload)
    assert resp.status_code == 401
    assert resp.json()['detail'] == "invalid password"
