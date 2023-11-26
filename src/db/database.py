import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncConnection,
    AsyncEngine,
)
from src.core.config import config
from src.db.base import Base


class DatabaseSessionManager:
    """
    Класс для управления сессиями базы данных в асинхронном контексте.

    Отвечает за инициализацию и закрытие соединения с базой данных.
    Предоставляет контекстные менеджеры для управления соединениями и сессиями.

    Методы:
    - init: Инициализирует движок базы данных и создает сессию.
    - close: Закрывает соединение с базой данных и удаляет сессию.
    - connect: Контекстный менеджер для создания асинхронного соединения.
    - session: Контекстный менеджер для управления асинхронными сессиями базы данных.
    - create_all: Создает все таблицы в базе данных.
    - drop_all: Удаляет все таблицы из базы данных.
    """

    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str = f"sqlite+aiosqlite:///{config.database.path}"):
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @staticmethod
    async def create_all(connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_all(connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


db_session_manager = DatabaseSessionManager()


async def get_db():
    """
    Асинхронный генератор для предоставления сессии базы данных.

    Использует DatabaseSessionManager для создания и управления сессиями базы данных.
    В случае исключения в контексте сессии выполняет откат транзакции.

    :return: Генератор, предоставляющий асинхронную сессию базы данных.
    """

    async with db_session_manager.session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
