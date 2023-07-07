"""stocks utils."""
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
    """
    Converts data read from external API into stock api data

    Parameters
    ----------
    stock_in : StockDataIn
        external api data

    Returns
    -------
    StockDataOut
        stock api data schema
    """
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
    """
    fetch stock data information using external API:
    https://www.alphavantage.co/documentation/

    Parameters
    ----------
    stock_url : str
        stocker url with blanks to be completed
    api_key : str
        stock api ky
    symbol : str
        stock symbol

    Returns
    -------
    StockDataIn
        stock data parsed schema

    Raises
    ------
    InvalidAPICall
        IF api fails because of symbol doesn't exist
    RemoteStockAPIError
        If api call fails for other reasons
    """
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
