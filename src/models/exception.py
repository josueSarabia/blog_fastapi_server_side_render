import json
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Any, Dict, Optional

class RequiresLoginException(StarletteHTTPException):
    """
    Class that handles and invalid user(not logged in) request.

    Args:
        status_code (int): status code,
        detail (str): more information about the error,
        headers (dict): headers of the error,
    """
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class ComplexEncoder(json.JSONEncoder):
    """
    Class that encodes a class into a json


    """
    def default(self, obj):
        """
        Method that encodes a class into a json

        Returns:
            the corresponding json encoding of the object
        """
        
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON() 
        elif type(obj).__name__ == 'UUID':
            return str(obj)
        elif type(obj).__name__ == 'datetime':
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
