"""General purpose constants"""
NAME_MAX_LENGTH = 50
LASTNAME_MAX_LENGTH = 50
DEFAULT_KEY_LENGTH = 16
STOCK_URL = (
    "https://www.alphavantage.co/query?"
    "function=TIME_SERIES_DAILY_ADJUSTED&"
    "symbol={symbol}&outputsize=compact&apikey={api_key}"
)
DEFAULT_STOCK_API_KEY = "X86NOH6II01P7R24"
DEFAULT_LIMITER_RULE = "5/minute"
