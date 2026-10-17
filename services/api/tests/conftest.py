import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.domain.models  # noqa: F401
import app.infrastructure.database.session as session_module
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import get_db
from app.main import app as fastapi_app

# Use shared-cache in-memory SQLite for testing with StaticPool so all async sessions share the connection
TEST_DATABASE_URL = "sqlite+aiosqlite:///file:testdb?mode=memory&cache=shared&uri=true"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

session_module.AsyncSessionLocal = TestSessionLocal


@pytest_asyncio.fixture(scope="function")
async def db_session():
    # Create all tables in test database
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    # Drop all tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def auth_headers_user1():
    return {"Authorization": "Bearer test-user-alice-123"}


@pytest.fixture
def auth_headers_user2():
    return {"Authorization": "Bearer test-user-bob-456"}
