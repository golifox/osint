from pydantic import BaseModel


class LinkSearchSchema(BaseModel):
    name: str
    url: str

    class Config:
        orm_mode = True


class LinkSchemaBase(LinkSearchSchema):
    category_id: int


class LinkSchemaCreate(LinkSchemaBase):
    pass


class LinkSchema(LinkSchemaBase):
    id: int

    class Config:
        orm_mode = True
