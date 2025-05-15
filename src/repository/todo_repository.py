from pydantic import UUID4
from sqlalchemy.orm import Session

from ..models.todo_models import ToDo
from ..schemas.toso_shcema import TodoInput, TodoOutput, TodoUpdate


from sqlalchemy.future import select
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

class TodoRepository:
    """
    Repository class for managing ToDo operations with the database (async version).
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: UUID4, data: TodoInput) -> TodoOutput:
        """
        Creates a new ToDo item for the specified user and returns the created item.
        """
        todo = ToDo(**data.model_dump(), created_by=user_id)
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)
        return todo

    async def get_todos_by_created_user(self, _created_by: UUID4) -> list[TodoOutput]:
        """
        Retrieve a list of todos created by a specific user.
        """
        result = await self.db.execute(select(ToDo).filter_by(created_by=_created_by))
        todos = result.scalars().all()
        return todos

    async def get_todos(self) -> list[TodoOutput]:
        """
        Retrieve all todo items from the database.
        """
        result = await self.db.execute(select(ToDo))
        todos = result.scalars().all()
        return todos

    async def get_single_todo(self, _id: int) -> TodoOutput | None:
        """
        Retrieve a single todo item by its ID.
        """
        result = await self.db.execute(select(ToDo).filter_by(id=_id))
        todo = result.scalar_one_or_none()
        return todo

    async def exists_todo_by_id_user(self, user_id: UUID4, _id: int) -> bool:
        """
        Checks if a ToDo item exists for a given user ID and ToDo ID.
        """
        result = await self.db.execute(
            select(ToDo).filter(ToDo.id == _id, ToDo.created_by == user_id)
        )
        todo = result.scalar_one_or_none()
        return todo is not None

    async def delete_todo_by_id(self, _id: int) -> None:
        """
        Deletes a ToDo item from the database by its ID.
        """
        await self.db.execute(delete(ToDo).filter_by(id=_id))
        await self.db.commit()

    async def update_todo_by_id(self, _id: int, data: TodoUpdate) -> TodoOutput | None:
        """
        Update a todo item by its ID with the provided data.
        """
        data_dict = data.model_dump(exclude_unset=True)
        await self.db.execute(update(ToDo).where(ToDo.id == _id).values(**data_dict))
        await self.db.commit()
        # Fetch updated todo
        result = await self.db.execute(select(ToDo).filter_by(id=_id))
        todo = result.scalar_one_or_none()
        return todo
