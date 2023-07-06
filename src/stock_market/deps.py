from typing import Generator
from stock_market.db.database import SessionLocal


def get_db() -> Generator:
    """Get a db Session.

    Yields:
        Generator: A db Session as a generator
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
