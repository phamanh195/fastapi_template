from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseUserSchema(BaseModel):
    """
    Schema share properties of "User" model.
    """

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = False
    is_superuser: Optional[bool] = False


class CreateUserSchema(BaseUserSchema):
    """
    Schema for creating user via API.
    """

    name: str
    email: EmailStr
    password: str


class UpdateUserSchema(BaseUserSchema):
    """
    Schema for updating user via API.
    """

    password: Optional[str]


class InDBUserSchema(BaseUserSchema):
    """
    Schema describe properties of "User" in database.
    """

    id: Optional[int] = None

    class Config:
        orm_mode = True


class RetrieveUserSchema(InDBUserSchema):
    """
    Schema for retrieving user via API.
    """
