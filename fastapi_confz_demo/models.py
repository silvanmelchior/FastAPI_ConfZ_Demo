from typing import Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
