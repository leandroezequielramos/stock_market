from fastapi import APIRouter
from stock_market.users.enpoints import users_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["users"])
