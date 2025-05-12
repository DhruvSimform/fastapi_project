from datetime import datetime
from enum import Enum

from sqlalchemy import (
    UUID,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.ext.hybrid import hybrid_property

from ..config.constant import ToDoStatus
from ..config.database import Base
from ..models.user_model import User


class ToDo(Base):

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    due_date = Column(Date, nullable=True)

    status = Column(Enum(ToDoStatus), default=ToDoStatus.pending, nullable=False)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now())

    created_by = Column(UUID, ForeignKey(User.id), nullable=False)

    @hybrid_property
    def is_overdue(self) -> bool:

        if (
            self.status != ToDoStatus.completed
            and self.due_date
            and self.due_date < datetime.now().date()
        ):
            return True
        return False

    @is_overdue.expression
    def check_is_over_due(cls):
        return (cls.status != ToDoStatus.completed) & (cls.due_date < func.now())
