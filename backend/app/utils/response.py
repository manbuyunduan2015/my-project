from typing import Optional, Any


def success_response(data: Optional[Any] = None, message: str = "success") -> dict:
    return {"code": 200, "message": message, "data": data}


def error_response(code: int = 400, message: str = "error") -> dict:
    return {"code": code, "message": message, "data": None}


def page_response(items: list, total: int, page: int = 1, page_size: int = 10) -> dict:
    return {"items": items, "total": total, "page": page, "page_size": page_size}
