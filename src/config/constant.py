from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class ToDoStatus(str, Enum):
    pending = "pending"
    inprogress = "inprogress"
    completed = "completed"
