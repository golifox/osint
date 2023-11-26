from sqlalchemy import String, ForeignKey, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, Mapped, mapped_column, selectinload

from src.db.base import Base


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship("Category", back_populates="links")

    def __repr__(self):
        return f"<Link(id={self.id}, name={self.name}, url={self.url})>"

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        transaction = cls(**kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, id: int):
        try:
            transaction = await db.get(cls, id)
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(cls, db: AsyncSession):
        return (await db.execute(select(cls))).scalars().all()

    @classmethod
    async def get_by_category_ids(cls, db: AsyncSession, category_ids: list[int, ...]):
        try:
            transaction = await db.execute(
                select(cls).filter(cls.category_id.in_(category_ids))
            )
        except NoResultFound:
            return None
        return transaction.scalars().all()


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    links: Mapped[list[Link]] = relationship(lazy="selectin")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        transaction = cls(**kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, id: int):
        try:
            transaction = await db.execute(
                select(cls).where(cls.id == id).options(selectinload(cls.links))
            )
        except NoResultFound:
            return None
        return transaction.scalar_one()

    @classmethod
    async def get_all(cls, db: AsyncSession):
        return (
            (await db.execute(select(cls).options(selectinload(cls.links))))
            .scalars()
            .all()
        )

    @classmethod
    async def get_by_name(cls, db: AsyncSession, name: str):
        try:
            transaction = await db.execute(
                select(cls).options(selectinload(cls.links)).where(cls.name == name)
            )
        except NoResultFound:
            return None

        return transaction.scalar_one_or_none()
