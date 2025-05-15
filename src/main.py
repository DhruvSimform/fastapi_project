import logging
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from src.config.settings import STATIC_DIR, settings
from src.router import auth_router, template_routes, todo_router, user_router
from src.utils.init_db import create_tables

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


# Mount static directory if it exists
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
async def on_startup():
    await create_tables()

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(todo_router.router)

app.include_router(template_routes.router)


# Configure logger only if needed (optional)
logger = logging.getLogger("process_time")
logger.setLevel(logging.INFO)


# Function-based middleware: fastest way
@app.middleware("http")
async def process_time_middleware(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Process-Time"] = f"{duration_ms} ms"

    # Logging optional: comment out to save performance
    print("-------------------------------------------------------")
    print(f"{request.method} {request.url.path} - {duration_ms} ms")
    logger.info(f"{request.method} {request.url.path} - {duration_ms} ms")

    return response


def main():
    uvicorn.run(app, port=8000, reload=True)


if __name__ == "__main__":
    main()
