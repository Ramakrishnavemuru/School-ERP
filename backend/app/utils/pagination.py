import math
from typing import Generic, List, TypeVar, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Query

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

def paginate_query(query: Query, page: int = 1, page_size: int = 20):
    page = max(1, page)
    page_size = max(1, min(100, page_size))
    total = query.count()
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }
