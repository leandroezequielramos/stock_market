from typing import Generator
from stock_market.db.database import SessionLocal


def get_db() -> Generator:
    """
    gets database session.

    Yields
    ------
    Generator
        A db session as a generator
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
