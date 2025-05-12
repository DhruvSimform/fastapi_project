from ..schemas.toso_shcema import TodoInput , TodoOutput
from ..repository.todo_repository import TodoRepository
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import UUID4


class TodoServices:

    def __init__(self,db: Session):
        self.repository = TodoRepository(db)

    def create_todo_for__user(self,_created_by: UUID4 ,data: TodoInput)  -> TodoOutput:
        return self.repository.create(_created_by , data)
    
    def get_list_of_todo_byuser(self, _created_by: UUID4 ) -> list[TodoOutput] :
        return self.repository.get_todos_by_created_user(_created_by)
    
    def get_single_todo(self , _id: UUID4) -> TodoOutput:
        return self.repository.get_single_todo(_id)

    def delete_todo(self , _id: UUID4) -> None:
        return self.repository.delete_todo_by_id(_id)
    
        