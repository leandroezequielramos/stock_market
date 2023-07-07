from datetime import date
from typing import OrderedDict, Dict, Union
from pydantic import BaseModel, Field


class StockMetadataIn(BaseModel):
    class Config:
        allow_population_by_field_name = True

    stock_name: str = Field(alias="2. Symbol")
    last_refresh: date = Field(alias="3. Last Refreshed")


class StockInfoIn(BaseModel):
    class Config:
        allow_population_by_field_name = True

    open: float = Field(alias="1. open")
    high: float = Field(alias="2. high")
    low: float = Field(alias="3. low")
    close: float = Field(alias="4. close")


class StockDataIn(BaseModel):
    class Config:
        allow_population_by_field_name = True

    stock_metadata: StockMetadataIn = Field(alias="Meta Data")
    stock_values: OrderedDict[date, StockInfoIn] = Field(
        alias="Time Series (Daily)"
    )


class MarketValueOut(BaseModel):
    open: float
    high: float
    low: float
    last_variation: float


class StockDataOut(BaseModel):
    name: str
    last_refresh: date
    market_value: MarketValueOut