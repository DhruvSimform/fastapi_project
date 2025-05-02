import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

app = FastAPI()


def main():
    uvicorn.run(app, port=8000, reload=True)


if __name__ == "__main__":
    load_dotenv()
    main()
