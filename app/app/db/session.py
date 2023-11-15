from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(
    str(settings.DB_SQLALCHEMY_URI), echo=settings.DEBUG, pool_pre_ping=True
)

AsyncDbSession = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)
