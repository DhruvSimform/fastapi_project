from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..repository.todo_repository import TodoRepository
from ..schemas.toso_shcema import TodoInput, TodoOutput, TodoUpdate


class TodoServices:
    """Service layer for handling Todo-related business logic."""

    def __init__(self, db: Session):
        self.repository = TodoRepository(db)

    def create_todo_for__user(self, _created_by: UUID4, data: TodoInput) -> TodoOutput:
        """Create a new todo item for the specified user."""
        return self.repository.create(_created_by, data)

    def get_list_of_todo_by_user(self, _created_by: UUID4) -> list[TodoOutput]:
        """Retrieve a list of todos created by a specific user."""
        return self.repository.get_todos_by_created_user(_created_by)

    def get_single_todo(self, _id: UUID4) -> TodoOutput:
        """Retrieve a single todo by its ID."""
        return self.repository.get_single_todo(_id)

    def get_single_todo_by_user(self, user_id, _id: UUID4) -> TodoOutput:
        """Retrieve a single todo by ID and verify ownership by user."""
        if not self.repository.exists_todo_by_id_user(user_id, _id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo does not exists"
            )
        return self.repository.get_single_todo(_id)

    def delete_todo(self, user_id, _id: UUID4) -> None:
        """Delete a todo if it exists and belongs to the user."""
        if not self.repository.exists_todo_by_id_user(user_id, _id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo does not exists"
            )
        return self.repository.delete_todo_by_id(_id)

    def update_todo(self, user_id, _id: UUID4, data: TodoUpdate) -> None:
        """Update a todo if it exists and belongs to the user."""
        if not self.repository.exists_todo_by_id_user(user_id, _id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo does not exists"
            )
        return self.repository.update_todo_by_id(_id, data)
