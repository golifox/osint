"""
Модуль для определения маршрутов API поиска.

Реализует функционал поиска по никнейму среди ссылок, принадлежащих определенным категориям.
Возвращает список результатов поиска, включающий информацию о ссылках и статусе поиска.
"""


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.shemas.links import LinkSearchSchema
from src.api.shemas.search import SearchSchemaCreate, SearchSchema
from src.db.database import get_db
from src.db.models import Link
from src.services.search_engine import SearchEngine

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/", response_model=list[SearchSchema])
async def search(payload: SearchSchemaCreate, db: AsyncSession = Depends(get_db)):
    links = await Link.get_by_category_ids(db, payload.category_ids)
    if links is None:
        links = await Link.get_all(db)

    result = []

    se = SearchEngine(links)
    async for link, result_url in se.search_nickname(payload.nickname):
        found = result_url is not None
        result.append(
            SearchSchema(
                link=LinkSearchSchema(**link.__dict__),
                found=found,
                found_link=result_url,
            )
        )

    return result
