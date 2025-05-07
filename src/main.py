import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from src.router import user_router
from src.utils.init_db import create_table
load_dotenv()
app = FastAPI()
create_table()
app.include_router(user_router.router)


def main():
    uvicorn.run(app, port=8000, reload=True)


if __name__ == "__main__":
    main()
