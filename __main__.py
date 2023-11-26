import asyncio
from src.core.helpers.categories_helper import input_category
from src.core.helpers.nickname_helper import input_nickname
from src.db.database import db_session_manager, get_db
from src.db.models import Category, Link
from src.services.search_engine import SearchEngine
from src.core.messages import *


# Основная асинхронная функция программы
async def main():
    # Инициализация менеджера сессий базы данных
    db_session_manager.init()

    # Бесконечный цикл для ввода данных пользователя и поиска
    while True:
        # Получение никнейма от пользователя
        nickname = input_nickname()

        # Получение списка всех категорий из базы данных
        async for session in get_db():
            categories = await Category.get_all(session)

        # Получение ID категорий от пользователя
        category_ids = input_category(categories)

        # Получение списка ссылок, соответствующих выбранным категориям
        async for session in get_db():
            links = await Link.get_by_category_ids(session, category_ids)

        # Создание экземпляра поискового движка и поиск по никнейму
        search_engine = SearchEngine(links)

        # Асинхронный перебор результатов поиска
        async for link, url in search_engine.search_nickname(nickname):
            # Определение статуса нахождения никнейма и вывод результата
            status = FOUND if url else NOT_FOUND
            print(f"{link.name}: {status} ({url if url else ''})")


# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(main())
