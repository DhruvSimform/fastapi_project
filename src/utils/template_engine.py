from pathlib import Path
from fastapi.templating import Jinja2Templates
from src.config.settings import TEMPLATES_DIR

if not Path(TEMPLATES_DIR).exists():
    raise RuntimeError(f"Templates directory not found: {TEMPLATES_DIR}")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
