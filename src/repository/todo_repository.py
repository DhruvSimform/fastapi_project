from pydantic import UUID4
from sqlalchemy.orm import Session
from ..schemas.toso_shcema import TodoInput , TodoOutput
from ..models.todo_models import ToDo

class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, _created_by: UUID4, data: TodoInput) -> TodoOutput:
        todo = ToDo(**data.model_dump(), created_by=_created_by)
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def get_todos_by_created_user(self, _created_by: UUID4) -> list[TodoOutput]:
        return self.db.query(ToDo).filter_by(created_by=_created_by).all()

    def get_todos(self) -> list[TodoOutput]:
        return self.db.query(ToDo).all()

    def get_single_todo(self, _id: int) -> TodoOutput:
        return self.db.query(ToDo).filter_by(id=_id).first()

    def exists_todo_by_id(self, _id: int) -> bool:
        return self.db.query(ToDo).filter_by(id=_id).first() is not None
    
    def delete_todo_by_id(self, _id: int) -> None:
        return self.db.query(ToDo).filter_by(id=_id).delete()
    


        
        