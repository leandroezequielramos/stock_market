"""stocks endpoints."""
from fastapi import APIRouter, HTTPException, Security, status
from starlette.requests import Request

from stock_market.auth import get_api_key
from stock_market.constants import STOCK_URL
from stock_market.exceptions import InvalidAPICall, RemoteStockAPIError
from stock_market.limiter import limiter
from stock_market.settings import settings
from stock_market.stocks.schemas import StockDataOut
from stock_market.stocks.utils import fetch_stock_data

stock_router = APIRouter()


@stock_router.get("")
@limiter.limit(settings.LIMITER_RULE)
async def get_stock_info(
    request: Request, stock_symbol: str, api_key: str = Security(get_api_key)
) -> StockDataOut:
    """
    gets stock information from external API and retrieve data to client

    Parameters
    ----------
    request : Request
        just for limiter requirements
    stock_symbol : str
        stock requested symbol
    api_key : str, optional
        api key, by default Security(get_api_key)

    Returns
    -------
    StockDataOut
        stock information

    Raises
    ------
    HTTPException (404)
        raised when stock symbol is not available
    HTTPException (400)
        raised when external api call fails
    """
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
