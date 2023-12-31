"""Users endpoint definition."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from stock_market.deps import get_db
from stock_market.exceptions import DBError, UserAlreadyRegistered
from stock_market.settings import settings
from stock_market.users.crud import user_crud
from stock_market.users.schemas import UserRegisterIn, UserRegisterOut
from stock_market.users.utils import generate_api_key

users_router = APIRouter()


@users_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserRegisterIn, db: Session = Depends(get_db)
) -> UserRegisterOut:
    """
    signup procedure. Takes user data, creates a user and answer with API KEY

    Parameters
    ----------
    user_data : UserRegisterIn
        User data from request
    db : Session, optional
        database session, by default Depends(get_db)

    Returns
    -------
    UserRegisterOut
        returns user api key

    Raises
    ------
    HTTPException
        Raise when user cannot be signedup
    """
    try:
        system_api_keys = user_crud.get_system_api_keys(db=db)
        result = user_crud.create(
            db=db,
            obj_in=user_data,
            api_key=generate_api_key(
                system_api_keys=system_api_keys, nbytes=settings.API_KEY_LENGTH
            ),
        )
    except (UserAlreadyRegistered, DBError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    return UserRegisterOut(api_key=result.api_key)


@users_router.get("/api_key")
async def get_user_api_key(
    user_email: EmailStr, db: Session = Depends(get_db)
) -> UserRegisterOut:
    """
    gets a user api key providing user email

    Parameters
    ----------
    user_email : EmailStr
        user email
    db : Session, optional
        database session, by default Depends(get_db)

    Returns
    -------
    UserRegisterOut
        user api key

    Raises
    ------
    HTTPException
        raised when user doesn't exist at database
    """
    user = user_crud.get_user_by_email(user_email=user_email, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRegisterOut(api_key=user.api_key)


@users_router.delete("", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(
    user_email: EmailStr, db: Session = Depends(get_db)
) -> str:
    """
    deletes a user from database using their email as id

    Parameters
    ----------
    user_email : EmailStr
        user email
    db : Session, optional
        database session, by default Depends(get_db)

    Returns
    -------
    str
        Message telling caller user was successfully deleted

    Raises
    ------
    HTTPException
        raised when user with email is not present at database
    """
    user = user_crud.delete_user_by_email(user_email=user_email, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return f"User {user_email} deleted"
