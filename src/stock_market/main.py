import uvicorn
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from stock_market.limiter import limiter
from stock_market.api import api_router
from stock_market.version import __API__VERSION
from stock_market.settings import settings


app = FastAPI(
    title="Stock Market API",
    description="An API for getting stock information",
    version=__API__VERSION,
    root_path=settings.ROOT_PATH,
    debug=settings.DEBUG_MODE,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/version")
async def version():
    return {"version": __API__VERSION}


app.include_router(api_router)


def start():
    uvicorn.run(
        settings.APP_MODULE,
        host=str(settings.HOST),
        port=settings.PORT,
        reload=True,
    )
