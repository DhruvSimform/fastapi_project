# FastAPI Project

This project showcases the features and capabilities of the FastAPI framework, which is ideal for building modern, high-performance web APIs.

## Features

- **Authentication**:
    - User registration and JWT-based login.
    - Token refresh and secure password hashing.

- **User Management**:
    - User account creation.
    - Profile view and update.
    - Admin-only field access (e.g., last login, user ID, and role).
    - Abstract data access based on roles with query optimization.
    - Normal users have limited access to view other users' data.
    - Retrieve all users with pagination support.

- **Todo Management**:
    - Create, retrieve, update, and delete tasks for logged-in users.
        - Input validation using Pydantic.
        - PostgreSQL database integration.
        - Custom error handling.

## Database Configuration

The database configuration is defined with the following settings:

- **`settings.DATABASE_URL`**: The connection string for the database.
- **`echo=True`**: Enables SQL query logging for debugging purposes.
- **`pool_size=3`**: Configures 3 connections per worker, resulting in a total of 12 connections for 4 workers.
- **`max_overflow=1`**: Allows up to 1 additional connection per worker, providing a maximum of 16 connections.
- **`pool_timeout=30`**: Specifies the wait time (in seconds) for a free connection before timing out.
- **`pool_pre_ping=True`**: Ensures stale connections are checked and reused efficiently.


## Requirements

This project requires the following:
- **Python 3.8+**: Ensure you have Python installed.
- **uv**: Python package manager for installing dependencies.
- **Uvicorn**: ASGI server for running the application.

To install uv, run:
```bash
pip install uv
```


## Installation

1. Clone the repository:
    ```bash
    git clone git@github.com:DhruvSimform/fastapi_project.git
    cd fastapi_project
    ```


2. Run the application in a virtual environment with its dependencies automatically installed and activated:
    ```bash
    uv run uvicorn src.main:app --reload
    ```
   - This command will create a `.venv` virtual environment, install all required dependencies, activate the environment, and start the application.


## Running the Application

Start the FastAPI application using Uvicorn:
```bash
uv run uvicorn src.main:app --reload
```

- The API will be available at `http://127.0.0.1:8000`.
- Swagger UI documentation: `http://127.0.0.1:8000/docs`
- ReDoc documentation: `http://127.0.0.1:8000/redoc`

## Project Structure

```text
fastapi_project/
├── src/
│   ├── config/          # Configuration files (settings, env vars)
│   ├── dependencies/    # Dependency injection and shared resources
│   ├── main.py          # Entry point of the application
│   ├── models/          # SQLAlchemy models
│   ├── repository/      # DB interactions and queries
│   ├── router/          # API route handlers (FastAPI routers)
│   ├── schemas/         # Pydantic models (request/response)
│   ├── service/         # Business logic and service layer
│   └── utils/           # Utility functions and helpers
├── templates/           # HTML templates for rendering views
├── statics/             # Static files (CSS, JS, images)
├── alembic/             # Database migrations folder
├── alembic.ini          # Alembic config file
├── pyproject.toml       # Project metadata and tool configs
├── uv.lock              # Locked dependency versions
├── requirements.txt     # List of Python dependencies
├── .gitignore           # Git ignored files/patterns
└── README.md            # Project documentation
```

```
## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.