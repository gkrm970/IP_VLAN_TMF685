from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncDbSession


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncDbSession()

    try:
        yield session
    finally:
        await session.close()
