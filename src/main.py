import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from src.router import auth_router, todo_router, user_router
from src.utils.init_db import create_table
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Project - User & Todo Management",
    description=(
        "This API provides functionality for user authentication, profile management, "
        "user account creation, and task management.\n\n"
        "**Features:**\n"
        "1. **Authentication**:\n"
        "   - User registration and JWT-based login.\n"
        "   - Token refresh and secure password hashing.\n\n"
        "2. **User Management**:\n"
        "   - User account creation.\n"
        "   - Profile view and update.\n"
        "   - Admin-only field access (e.g., last login, user ID, and role).\n"
        "   - Abstract data access based on roles with query optimization.\n"
        "   - Normal users have limited access to view other users' data.\n\n"
        "3. **Todo Management**:\n"
        "   - Create, retrieve, update, and delete tasks for logged-in users.\n"
        "   - Input validation using Pydantic.\n"
        "   - PostgreSQL database integration.\n"
        "   - Custom error handling."
    ),
    contact={
        "name": "Dhruv Patel",
        "email": "pateldhruvn2004@gmail.com",
        "url": "https://github.com/DhruvSimform",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Endpoints for user login and token management.",
        },
        {
            "name": "Users",
            "description": (
                "Endpoints for user profile management, user account creation, and admin-level operations.\n"
                "- Normal users can only view limited profile data of other users.\n"
                "- Admin users can view all fields, including last login, user ID, and role."
            ),
        },
        {
            "name": "Todo",
            "description": "Endpoints for managing to-do tasks with CRUD operations.",
        },
    ],
    version="1.0.0",
)



create_table()

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(todo_router.router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def main():
    uvicorn.run(app, port=8000, reload=True)


if __name__ == "__main__":
    main()
