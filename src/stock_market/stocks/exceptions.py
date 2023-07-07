from typing import List, Any


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
    exception raised when and identifier is not a uuid valid
    """

    def __init__(self, reason):
        super(InvalidAPICall, self).__init__(msg=f"INVALID CALL: {reason}")
