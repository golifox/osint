from pydantic import BaseModel

from src.api.shemas.links import LinkSearchSchema


class SearchSchemaBase(BaseModel):
    pass


class SearchSchemaCreate(SearchSchemaBase):
    nickname: str
    category_ids: list[int] = []


class SearchSchema(SearchSchemaBase):
    link: LinkSearchSchema
    found: bool
    found_link: str | None = None
