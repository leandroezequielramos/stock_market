from pydantic import BaseModel, constr, EmailStr


class UserRegisterIn(BaseModel):
    name: constr(min_length=1, max_length=50)
    lastname: constr(min_length=1, max_length=50)
    email: EmailStr


class UserRegisterOut(BaseModel):
    api_key: str
