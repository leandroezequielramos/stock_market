"""Defines authentication mechanism."""
from fastapi import HTTPException, status, Security, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from stock_market.deps import get_db
from stock_market.users.crud import user_crud

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def get_api_key(
    api_key_header: str = Security(api_key_header),
    db: Session = Depends(get_db),
) -> str:
    """
    gets api key from request an evaluate if it's allowed

    Parameters
    ----------
    api_key_header : str, optional
        api key, by default Security(api_key_header)
    db : Session, optional
        database session, by default Depends(get_db)

    Returns
    -------
    str
        api key if valid

    Raises
    ------
    HTTPException
        a 401(Unauthorized) exception when api key is not present or invalid
    """
    if api_key_header and user_crud.get_user_by_api_key(
        api_key=api_key_header, db=db
    ):
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
