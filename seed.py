import os
import aiosqlite

from src.core.config import config
from src.core.logger import osint_logger as logger


async def find_or_insert_link(cursor, category_id, name, url):
    await cursor.execute("SELECT * FROM links WHERE name = ? AND url = ?", (name, url))
    if not await cursor.fetchone():
        await cursor.execute(
            "INSERT INTO links (name, url, category_id) VALUES (?, ?, ?)",
            (name, url, category_id),
        )
        logger.info(f"Добавлена ссылка {name}")


async def find_or_insert_category(cursor, category_name):
    await cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    category = await cursor.fetchone()
    if not category:
        await cursor.execute(
            "INSERT INTO categories (name) VALUES (?)", (category_name,)
        )
        category_id = cursor.lastrowid
        logger.info(f"Добавлена категория {category_name}")
    else:
        category_id = category[0]

    return category_id


async def parse_file(cursor, file_path, category_id):
    unique_links = set()
    with open(file_path, "r") as file:
        for line in file:
            name, url = line.strip().split(" ", 1)
            if (name, url) not in unique_links:
                unique_links.add((name, url))
                await find_or_insert_link(cursor, category_id, name, url)


async def parse_directory(directory):
    async with aiosqlite.connect(config.database.path) as db:
        cursor = await db.cursor()
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                category_name = os.path.splitext(filename)[0]
                category_id = await find_or_insert_category(cursor, category_name)
                await parse_file(cursor, file_path, category_id)
        await db.commit()


import asyncio

asyncio.run(parse_directory("data/sites"))
