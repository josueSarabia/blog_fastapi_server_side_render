import json
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Any, Dict, Optional

class RequiresLoginException(StarletteHTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON() 
        elif type(obj).__name__ == 'UUID':
            return str(obj)
        elif type(obj).__name__ == 'datetime':
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
