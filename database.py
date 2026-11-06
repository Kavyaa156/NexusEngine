from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from models_db import Base

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/nexus_engine"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Add this utility function to build tables physically
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session