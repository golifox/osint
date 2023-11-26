from pydantic import BaseModel

from src.api.shemas.links import LinkSchema


class CategorySchemaBase(BaseModel):
    name: str


class CategorySchemaCreate(CategorySchemaBase):
    pass


class CategorySchema(CategorySchemaBase):
    id: int

    class Config:
        orm_mode = True


class CategorySearchSchema(CategorySchema):
    pass


class CategoryWithLinksSchema(CategorySchema):
    links: list[LinkSchema]

    class Config:
        orm_mode = True
