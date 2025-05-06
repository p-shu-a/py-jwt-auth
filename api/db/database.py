from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "postgresql+asyncpg://token_master@localhost:5432/jwt_users"
# create a async db connection:
engine = create_async_engine(DATABASE_URL, echo=True)

# create a session for db use
# its a "session factory" that is, it gets you a fresh db session on demand
async_session = sessionmaker(
                    bind=engine, 
                    class_=AsyncSession, 
                    expire_on_commit=False
)

# this is intersting...
# provides a baseclass to register object (class) to DB Table
Base = declarative_base()

async def get_session():
    async with async_session() as session:
        yield session

