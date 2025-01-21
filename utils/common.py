from typing import Any, Dict

# Function to return a success response
def success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    return {"success": True, "message": message, "data": data if data else []}

# Function to return an error response
def error_response(message: str, error_code: int, data: Any = None) -> Dict[str, Any]:
    return {"success": False, "message": message, "error_code": error_code, "data": []}
