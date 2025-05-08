import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.app import api
from api.db.database import get_db_session

TEST_DATABASE_URL = "postgresql+asyncpg://token_master@localhost:5432/jwt_test"

test_engine = create_async_engine(TEST_DATABASE_URL)

test_session = sessionmaker(
                bind=test_engine, 
                class_=AsyncSession, 
                expire_on_commit=False
)

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# override api dependancy...
# automatically, before every
@pytest_asyncio.fixture(scope="function", autouse=True)
async def override_get_db_session():
    async def override():
        async with test_session() as session:
            yield session
    api.dependency_overrides[get_db_session] = override
    yield
    api.dependency_overrides.clear()

import asyncio
