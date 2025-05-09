import pytest_asyncio
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import asyncio
from api.app import api
from api.db.database import get_db_session
from httpx import ASGITransport, AsyncClient
import os

# moved to docker_compose
#TEST_DATABASE_URL = "postgresql+asyncpg://token_master@localhost:5432/jwt_test"
TEST_DATABASE_URL = os.genenv("TEST_DATABASE_URL")

test_engine = create_async_engine(
    TEST_DATABASE_URL, 
    poolclass=NullPool          # this was the fix!
)

test_session = sessionmaker(
                bind=test_engine, 
                class_=AsyncSession, 
                expire_on_commit=False
)

# override api dependancy...
# automatically, before every test and then clear the over ride
@pytest_asyncio.fixture(scope="function", autouse=True)
async def override_get_db_session():
    async def override():
        async with test_session() as session:
            yield session
    api.dependency_overrides[get_db_session] = override
    yield
    api.dependency_overrides.clear()


''' 
    - whats happening above?
    - What does the second yield do? It pauses execution, and "yields to the test calling the fixture
    - let the test work. Once the execution is finished, then come back clear()
    - generators, after the yield call, can continue execution
        - That to me really does seem like the main difference between a generator and a regular function

    Note: 
    - Generators are kind of like decorators in the sense that they wrap something...
        - With decorators they wrap a function, explicitly.
        - Whereas a generator "wraps" around a yield. 
        - They both do something before and after the return or yield
'''

# an async client is a way to "in-memory" the database. 
# this way, the tests can happen without spinning up a real server
# it acts like a real client
@pytest_asyncio.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=api)
    async with AsyncClient(transport=transport, base_url="http://jwt_test") as client:
        yield client