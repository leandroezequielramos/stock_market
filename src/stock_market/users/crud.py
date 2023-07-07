from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from stock_market.users.models import UserModel
from stock_market.users.schemas import UserRegisterIn
from stock_market.exceptions import UserAlreadyRegistered, DBError


class CRUDUser:
    def __init__(self):
        self._model = UserModel

    def get_all(self, db: Session) -> List[UserModel]:
        return db.query(self._model).all()

    def get_system_api_keys(self, db: Session) -> List[str]:
        users = user_crud.get_all(db=db)
        return [user.api_key for user in users]

    def get_user_by_email(
        self, user_email: str, db: Session
    ) -> Optional[UserModel]:
        return (
            db.query(self._model)
            .filter(self._model.email == user_email)
            .first()
        )

    def delete_user_by_email(
        self, user_email: str, db: Session
    ) -> Optional[UserModel]:
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
        return (
            db.query(self._model)
            .filter(self._model.api_key == api_key)
            .first()
        )

    def create(
        self, db: Session, *, obj_in: UserRegisterIn, api_key: str
    ) -> UserModel:
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
