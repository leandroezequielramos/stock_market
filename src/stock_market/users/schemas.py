"""Defines user schemas"""
from pydantic import BaseModel, EmailStr, constr


class UserRegisterIn(BaseModel):
    """Schema used for getting user registration data from request"""

    name: constr(min_length=1, max_length=50)
    lastname: constr(min_length=1, max_length=50)
    email: EmailStr


class UserRegisterOut(BaseModel):
    """Schema used to respond user registration"""

    api_key: str
