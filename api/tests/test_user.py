from fastapi.testclient import TestClient
from api.models.user import RegisterUser
from api.core.globals import master_user_db
from api.app import api
import time
client = TestClient(api)

TEST_USER_RESUABLE = RegisterUser("joan_holloway",
                                  "office_space",
                                  "internet",
                                  "127.0.0.1",
                                  int(time.time()))

TEST_USER_RESUABLE_JSON = {"username": "joan_holloway",
                           "password": "office_space"}

# test saving a new user
def test_register_new_user():
    payload = {"username":f"joan_holloway_{time.time()}", "password":"office_space"}
    resp = client.post("/register", json=payload)
    assert resp.status_code == 201
    assert resp.json() == {"message" : f"{TEST_USER_RESUABLE_JSON['username']} registerd successfully"}

# Test saving an existing user.
def test_register_existing_user():
    
    resp = client.post("/register", json=TEST_USER_RESUABLE_JSON)
    assert resp.status_code == 401
    assert resp.json() == {"detail": "user already registerd"}

# what if the user sending in junk json?
# we'll pydantic does most of the heavy lifting.
# its expecting a particular set of keys
# when the expected keys don't come it, it responds with a 422 and a wackass body...
def test_register_user_bad_json():
    payload = {"usernam": "foo_bar",
               "pa55w0rd": "bar_foo"}
    
    resp = client.post("/register", json=payload)
    assert resp.status_code == 422

# try to log in as some non-existing user
def test_login_non_exist():
    payload = {"username":"john_cena",
               "password":"you_cant_see_mee"}
    resp = client.post("/login", json=payload)
    assert resp.status_code == 404
    assert resp.json() == {"detail":f"{payload['username']} not found. register first"}

# test logging in with an existing user
def test_login_existing_user():
    
    resp = client.post("/login", json=TEST_USER_RESUABLE_JSON)
    assert resp.status_code == 201
    resp_body = resp.json()
    assert "auth_token" in resp_body
    assert resp_body['success'] == f"{TEST_USER_RESUABLE_JSON['username']} logged in"

# user exists but password is incorrect
def test_existing_user_wrong_password():

    payload = {"username":TEST_USER_RESUABLE_JSON['username'],
               "password": "peggy_sue"}
    resp = client.post("/login", json=payload)
    assert resp.status_code == 401
    assert resp.json()['detail'] == "invalid password"

