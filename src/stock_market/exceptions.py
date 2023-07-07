"""Exceptions definition."""
from typing import Any


class StockException(Exception):
    """
    Base class for exception hierarchy
    """

    def __init__(self, msg: str):
        """
        class constructor
        Parameters
        ----------
        msg: str
            Message to be shown
        """
        self._msg = msg

    @staticmethod
    def _obj_to_str(obj: Any) -> str:
        """
        converts an object of Any type to str
        Parameters
        ----------
        obj : Any
            object
        Returns
        -------
        str
            String representation of object
        """
        return "<None object>" if obj is None else str(obj)

    def __str__(self) -> str:  # pragma: no cover
        """
        show exception as string
        Returns
        -------
        str
            exception as string
        """
        return self._msg


class InvalidAPICall(StockException):
    """
    exception raised when API call fails
    """

    def __init__(self, reason: str):
        """
        class constructor

        Parameters
        ----------
        reason : str
            reason of failure
        """
        super(InvalidAPICall, self).__init__(msg=f"INVALID CALL: {reason}")


class RemoteStockAPIError(StockException):
    """
    exception raised when remote API call fails
    """

    def __init__(self):
        """
        class constructor
        """
        super(RemoteStockAPIError, self).__init__(
            msg=f"stock information is unreachable"
        )


class UserAlreadyRegistered(StockException):
    """
    exception raised when try to register an already registered user
    """

    def __init__(self, email: str):
        """
        class constructor

        Parameters
        ----------
        email : str
            user email
        """
        super(UserAlreadyRegistered, self).__init__(
            msg=f"User with {email} already registered"
        )


class DBError(StockException):
    """
    exception raised when API call fails
    """

    def __init__(self):
        """
        class constructor
        """
        super(DBError, self).__init__(msg=f"Imposible to reach data")
