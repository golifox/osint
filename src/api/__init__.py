from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.db.database import db_session_manager as sessionmanager, get_db


def init_app(init_db=True):
    """
    Инициализирует и конфигурирует экземпляр FastAPI приложения.

    Создает и настраивает приложение FastAPI с опциональной инициализацией базы данных.
    Если параметр init_db установлен в True, инициализирует менеджер сессий базы данных и выполняет создание всех необходимых таблиц.
    Конфигурирует маршрутизацию и CORS для приложения.

    :param init_db: Флаг, указывающий на необходимость инициализации базы данных при запуске приложения.

    :return: сконфигурированный экземпляр приложения FastAPI.
    """

    lifespan = None

    if init_db:
        sessionmanager.init()
        sessionmanager.create_all(get_db)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    server = FastAPI(title="FastAPI server", lifespan=lifespan)

    server.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from src.api.views.categories import router as category_router
    from src.api.views.links import router as link_router
    from src.api.views.search import router as search_router

    server.include_router(category_router, prefix="/api", tags=["category"])
    server.include_router(link_router, prefix="/api", tags=["link"])
    server.include_router(search_router, prefix="/api", tags=["search"])

    return server
