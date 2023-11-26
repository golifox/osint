"""
Модуль для определения маршрутов API, связанных со ссылками.

Предоставляет маршрут для получения списка всех ссылок в системе.
"""


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.shemas.links import LinkSchema
from src.db.database import get_db
from src.db.models import Link

router = APIRouter(prefix="/links", tags=["link"])


@router.get("/", response_model=list[LinkSchema])
async def get_links(db: AsyncSession = Depends(get_db)):
    categories = await Link.get_all(db)
    return categories
