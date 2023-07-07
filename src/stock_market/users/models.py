"""Defines user models."""
from sqlalchemy import Column, Integer, String
from stock_market.db.database import Base


class UserModel(Base):
    """User database model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=False)
    lastname = Column(String, unique=False, index=False)
    email = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True, index=True)
