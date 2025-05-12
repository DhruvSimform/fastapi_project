from pydantic import BaseModel, UUID4
from datetime import datetime
from ..config.constant import ToDoStatus
import uuid

class Todo(BaseModel):
    model_config = {"from_attributes": True}

class TodoInDB(Todo):
    id: int
    title: str
    description: str
    due_date: datetime
    status: ToDoStatus

    created_at: datetime
    updated_at: datetime

    created_by: UUID4

class TodoInput(BaseModel):
    title: str
    description: str
    due_date: datetime | None = None
    status: ToDoStatus = ToDoStatus.pending

class TodoOutput(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    status: ToDoStatus
    is_over_due: bool

    created_at: datetime
    updated_at: datetime

