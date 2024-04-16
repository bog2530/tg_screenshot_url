from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from worker.db import Statistics


class BaseRepository:
    _model = Statistics

    def __init__(self, db: str):
        self._session = async_sessionmaker(create_async_engine(db))

    async def save(self, entity) -> None:
        """
        Сохранение статистики
        """
        async with self._session.begin() as session:
            session.add(entity)
            await session.flush([entity])
