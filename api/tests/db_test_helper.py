import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from api.app import api
from api.db.database import get_db_session



TEST_DATABASE_URL = "postgresql+asyncpg://token_master@localhost:5432/jwt_test"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

test_session = sessionmaker(
                bind=test_engine, 
                class_=AsyncSession, 
                expire_on_commit=False
)


# override api dependancy...
# automatically, before every
@pytest.fixture(autouse=True)
async def override_get_session():
    async def override():
        async with test_session() as session:
            yield session
    api.dependency_overrides[get_db_session] = override
    yield
    api.dependency_overrides.clear()
