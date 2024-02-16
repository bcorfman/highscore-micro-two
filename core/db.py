from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import starlette_config


class DBSetup:

    def __init__(self):
        self._database_url = starlette_config.get("ELEPHANTSQL_URL")
        self.engine = create_async_engine(self._database_url, echo=False)

    async def _create_tables(self):
        # creates tables if they don't exist already; otherwise, leaves them alone.
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def get_session(self):
        await self._create_tables()
        async_session = sessionmaker(self.engine,
                                     class_=AsyncSession,
                                     expire_on_commit=False)
        async with async_session() as session:
            yield session
