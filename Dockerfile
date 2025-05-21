FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app
COPY . .
RUN uv sync --locked


# Make the start script executable
RUN chmod +x ./start.sh

# Expose FastAPI default port
EXPOSE 8000

# Start FastAPI with uv run (loads .env automatically)

# Run the script inside the uv environment
CMD ["uv", "run", "--", "./start.sh"]