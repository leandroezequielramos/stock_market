"""Defines user schemas"""
from pydantic import BaseModel, EmailStr, constr
from stock_market.constants import NAME_MAX_LENGTH, LASTNAME_MAX_LENGTH


class UserRegisterIn(BaseModel):
    """Schema used for getting user registration data from request"""

    name: constr(min_length=1, max_length=NAME_MAX_LENGTH)
    lastname: constr(min_length=1, max_length=LASTNAME_MAX_LENGTH)
    email: EmailStr


class UserRegisterOut(BaseModel):
    """Schema used to respond user registration"""

    api_key: str
