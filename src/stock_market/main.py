from typing import Union
import uvicorn
from fastapi import FastAPI
from stock_market.api import api_router
from stock_market.version import __API__VERSION
from stock_market.settings import settings

app = FastAPI()


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
