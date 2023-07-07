import requests
from datetime import date, timedelta
from fastapi import HTTPException, status
from stock_market.stocks.schemas import (
    StockDataIn,
    StockDataOut,
    MarketValueOut,
)
from stock_market.exceptions import InvalidAPICall, RemoteStockAPIError
from stock_market.logger import get_logger


logger = get_logger("APICall")


def _convert_stock_data_output(stock_in: StockDataIn) -> StockDataOut:
    variation = (
        stock_in.stock_values[stock_in.stock_metadata.last_refresh].close
        - stock_in.stock_values[
            stock_in.stock_metadata.last_refresh - timedelta(days=1)
        ].close
    )
    last_stock_info = stock_in.stock_values[
        stock_in.stock_metadata.last_refresh
    ]
    return StockDataOut(
        name=stock_in.stock_metadata.stock_name,
        last_refresh=stock_in.stock_metadata.last_refresh,
        market_value=MarketValueOut(
            open=last_stock_info.open,
            high=last_stock_info.high,
            low=last_stock_info.low,
            last_variation=variation,
        ),
    )


def fetch_stock_data(stock_url: str, api_key: str, symbol: str) -> StockDataIn:
    replaced_stock_url = stock_url.format(symbol=symbol, api_key=api_key)
    logger.debug(f"API request url: {replaced_stock_url}")
    resp = requests.get(replaced_stock_url)
    logger.debug(f"Response: status={resp.status_code}, data = {resp.json()}")
    data = resp.json()
    if "Error Message" in data.keys():
        raise InvalidAPICall(data["Error Message"])
    if "Meta Data" not in data.keys():
        raise RemoteStockAPIError()
    stock_in = StockDataIn.parse_obj(data)
    return _convert_stock_data_output(stock_in=stock_in)
