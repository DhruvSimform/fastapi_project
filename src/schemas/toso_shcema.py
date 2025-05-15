from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..config.constant import ToDoStatus  # Assuming this is your Enum


class Todo(BaseModel):
    """Base model for todo shared config."""

    model_config = {"from_attributes": True}


class TodoInput(Todo):
    """Input schema for creating a new todo item."""

    title: str = Field(
        ...,
        title="Title",
        description="Short title of the task.",
        example="Buy groceries",
        min_length=1,
        max_length=100,
    )
    description: str = Field(
        ...,
        title="Description",
        description="Detailed description of the task.",
        example="Buy milk, bread, and eggs from the store.",
    )
    due_date: date | None = Field(
        None,
        title="Due Date",
        description="Date the task should be completed by (optional).",
        example="2025-05-20",
    )
    status: ToDoStatus = Field(
        default=ToDoStatus.pending,
        title="Status",
        description="Current status of the task.",
        example="pending",
    )


class TodoInDB(Todo):
    """Schema representing a todo item stored in the database."""

    id: int
    title: str
    description: str
    due_date: date
    status: ToDoStatus
    created_at: datetime
    updated_at: datetime
    created_by: UUID


class TodoOutput(Todo):
    """Public-facing todo schema for API responses."""

    id: int
    title: str
    description: str
    due_date: date
    status: ToDoStatus

    is_overdue: bool = Field(
        ...,
        title="Is Overdue",
        description="Indicates if the task is past its due date.",
    )

    created_at: datetime
    updated_at: datetime


class TodoUpdate(Todo):
    """Schema for updating a todo item."""

    title: str | None = Field(
        None,
        title="Title",
        description="Updated title of the task (optional).",
        example="Get groceries",
    )
    description: str | None = Field(
        None,
        title="Description",
        description="Updated description of the task (optional).",
        example="Include fruits as well.",
    )
    due_date: date | None = Field(
        None,
        title="Due Date",
        description="Updated due date (optional).",
        example="2025-06-01",
    )
    status: ToDoStatus | None = Field(
        None,
        title="Status",
        description="Updated task status (optional).",
        example="inprogress",
    )
