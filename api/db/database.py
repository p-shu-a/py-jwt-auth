from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://token_master@localhost:5432/jwt_users"
# create a async db connection:

prod_engine = create_async_engine(DATABASE_URL)

# create a session for db use
# its a "session factory." that is, it creates a fresh db session on demand
prod_async_session = sessionmaker(
                        bind=prod_engine, 
                        class_=AsyncSession, 
                        expire_on_commit=False
)

# this function gets called as a dependency into the routers using FastApi's Depends() keyword
# the function itself is a generator calling the session_maker above. It yields a session...
async def get_db_session():
    async with prod_async_session() as session:
        yield session


# the declarative base class is part of the sqlAlchemy's alchemy...
# An object into a DataBase table. Used in the user's model. 
Base = declarative_base()