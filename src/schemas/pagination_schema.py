from typing import Generic, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class PaginatedResponse[DataT](BaseModel):
    total: int  # Total number of items
    total_pages: int  # Total number of pages
    page: int  # Current page number
    size: int  # Items per page
    data: list[DataT]  # Actual items for this page
    has_next: bool  # Indicates if there is a next page
    has_previous: bool  # Indicates if there is a previous page
    next_page_url: str | None = None  # URL of the next page or None
    previous_page_url: str | None = None  # URL of the previous page or None


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number, starting from 1")
    limit: int = Field(
        10, ge=1, le=100, description="Number of items per page, max 100"
    )
