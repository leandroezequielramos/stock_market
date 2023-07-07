"""Defines User CRUD"""
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from stock_market.exceptions import DBError, UserAlreadyRegistered
from stock_market.users.models import UserModel
from stock_market.users.schemas import UserRegisterIn


class CRUDUser:
    """
    CRUD user class definition
    """

    def __init__(self):
        """
        class constructor
        """
        self._model = UserModel

    def get_all(self, db: Session) -> List[UserModel]:
        """
        gets all users in database

        Parameters
        ----------
        db : Session
            an opened database session

        Returns
        -------
        List[UserModel]
            a list with user models
        """
        return db.query(self._model).all()

    def get_system_api_keys(self, db: Session) -> List[str]:
        """
        retrieves all system generated api keys valid

        Parameters
        ----------
        db : Session
            database session

        Returns
        -------
        List[str]
            List of system active api keys
        """
        users = user_crud.get_all(db=db)
        return [user.api_key for user in users]

    def get_user_by_email(
        self, user_email: str, db: Session
    ) -> Optional[UserModel]:
        """
        gets a user by email. return None if user is not found

        Parameters
        ----------
        user_email : str
            user email
        db : Session
            database session

        Returns
        -------
        Optional[UserModel]
            UserModel for user with email or None if not exist on db
        """
        return (
            db.query(self._model)
            .filter(self._model.email == user_email)
            .first()
        )

    def delete_user_by_email(
        self, user_email: str, db: Session
    ) -> Optional[UserModel]:
        """
        deletes a user from database using their email as key.


        Parameters
        ----------
        user_email : str
            user email
        db : Session
            database session

        Returns
        -------
        Optional[UserModel]
            user model or None if not present.

        Raises
        ------
        DBError
            Error when database is unreachable or something wrong happens
        """
        try:
            obj = (
                db.query(self._model)
                .filter(self._model.email == user_email)
                .first()
            )
            if obj:
                db.delete(obj)
                db.commit()
        except IntegrityError as e:
            raise DBError() from error
        return obj

    def get_user_by_api_key(
        self, api_key: str, db: Session
    ) -> Optional[UserModel]:
        """
        gets a user using their api key

        Parameters
        ----------
        api_key : str
            api key
        db : Session
            database session

        Returns
        -------
        Optional[UserModel]
            user or None if api key is not present in db.
        """

        return (
            db.query(self._model)
            .filter(self._model.api_key == api_key)
            .first()
        )

    def create(
        self, db: Session, *, obj_in: UserRegisterIn, api_key: str
    ) -> UserModel:
        """
        creates a new user

        Parameters
        ----------
        db : Session
            database connection
        obj_in : UserRegisterIn
            User data schema
        api_key : str
            generated api key

        Returns
        -------
        UserModel
            a new created user

        Raises
        ------
        UserAlreadyRegistered
            raised when user email already exists in database
        DBError
            raise when database error occurs
        """
        try:
            obj_in_data = jsonable_encoder(obj_in, by_alias=False)
            obj_in_data.update({"api_key": api_key})
            db_obj = self._model(**obj_in_data)  # type: ignore
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except IntegrityError as e:
            raise UserAlreadyRegistered(email=db_obj.email) from e
        except SQLAlchemyError as e:
            raise DBError() from e
        return db_obj


user_crud = CRUDUser()
