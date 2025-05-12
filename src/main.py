import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from src.router import auth_router, todo_router, user_router
from src.utils.init_db import create_table

load_dotenv()

app = FastAPI()

create_table()

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(todo_router.router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def main():
    uvicorn.run(app, port=8000, reload=True)


if __name__ == "__main__":
    main()
