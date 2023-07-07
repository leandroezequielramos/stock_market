import requests
from datetime import date, timedelta
from fastapi import HTTPException, status
from stock_market.stocks.schemas import (
    StockDataIn,
    StockDataOut,
    MarketValueOut,
)
from stock_market.stocks.exceptions import InvalidAPICall


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
    r = requests.get(stock_url.format(symbol=symbol, api_key=api_key))
    data = r.json()
    if "Error Message" in data.keys():
        raise InvalidAPICall(data["Error Message"])
    stock_in = StockDataIn.parse_obj(data)
    return _convert_stock_data_output(stock_in=stock_in)
