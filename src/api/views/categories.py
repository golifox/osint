"""
Модуль для определения маршрутов API, связанных с категориями.

Маршруты включают получение списка всех категорий, получение конкретной категории по ID,
а также получение всех ссылок, принадлежащих определенной категории.
"""


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.shemas.categories import CategoryWithLinksSchema
from src.api.shemas.links import LinkSchema
from src.db.database import get_db
from src.db.models import Category

router = APIRouter(prefix="/categories", tags=["category"])


@router.get("/", response_model=list[CategoryWithLinksSchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    categories = await Category.get_all(db)
    return categories


@router.get("/{category_id}", response_model=CategoryWithLinksSchema)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await Category.get(db, category_id)
    return category


@router.get("/{category_id}/links", response_model=list[LinkSchema])
async def get_category_links(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await Category.get(db, category_id)
    return category.links
