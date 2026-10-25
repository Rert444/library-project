from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)