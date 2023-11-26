from src.api import init_app

if __name__ == "__main__":
    """
    Точка входа для запуска FastAPI приложения с использованием Uvicorn.

    Конфигурирует и запускает ASGI сервер на указанном хосте и порту.
    Использует функцию `init_app` для инициализации и настройки приложения FastAPI.
    """

    import uvicorn

    uvicorn.run(init_app(), host="0.0.0.0", port=8000)
