"""Defines routes for the entire API."""
from fastapi import APIRouter

from stock_market.stocks.endpoints import stock_router
from stock_market.users.enpoints import users_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(stock_router, prefix="/stocks", tags=["stocks"])
