import uuid
from datetime import date , datetime

from pydantic import UUID4, BaseModel


from ..config.constant import ToDoStatus


class Todo(BaseModel):
    model_config = {"from_attributes": True}


class TodoInDB(Todo):
    id: int
    title: str
    description: str
    due_date: date
    status: ToDoStatus

    created_at: datetime
    updated_at: datetime

    created_by: UUID4


class TodoInput(Todo):
    title: str
    description: str
    due_date: date | None = None
    status: ToDoStatus = ToDoStatus.pending


class TodoOutput(Todo):
    id: int
    title: str
    description: str
    due_date: date
    status: ToDoStatus
    is_overdue: bool

    created_at: datetime
    updated_at: datetime


class TodoUpdate(Todo):
    title: str | None = None
    description: str | None = None
    due_date: date | None = None
    status: ToDoStatus | None = None
