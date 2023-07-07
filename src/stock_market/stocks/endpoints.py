from fastapi import APIRouter, Security, HTTPException, status
from starlette.requests import Request
from stock_market.settings import settings
from stock_market.constants import STOCK_URL
from stock_market.auth import get_api_key
from stock_market.stocks.utils import fetch_stock_data
from stock_market.exceptions import InvalidAPICall, RemoteStockAPIError
from stock_market.limiter import limiter

stock_router = APIRouter()


@stock_router.get("")
@limiter.limit(settings.LIMITER_RULE)
async def get_stock_info(
    request: Request, stock_symbol: str, api_key: str = Security(get_api_key)
):
    try:
        stock_data = fetch_stock_data(
            stock_url=STOCK_URL,
            api_key=settings.STOCK_API_KEY,
            symbol=stock_symbol,
        )
    except InvalidAPICall as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"stock {stock_symbol} not found",
        ) from e
    except RemoteStockAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock information is not available",
        ) from e
    return stock_data
