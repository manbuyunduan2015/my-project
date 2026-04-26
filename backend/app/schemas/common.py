from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar

T = TypeVar("T")


class Result(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None


class PageResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
