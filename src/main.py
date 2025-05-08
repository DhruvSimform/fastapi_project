import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from src.router import user_router , auth_router
from src.utils.init_db import create_table
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

app = FastAPI()

create_table()

app.include_router(auth_router.router)
app.include_router(user_router.router)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def main():
    uvicorn.run(app, port=8000, reload=True)


if __name__ == "__main__":
    main()
