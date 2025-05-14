from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse

from ..config.settings import settings
from ..utils.template_engine import templates

router = APIRouter(tags=["Templates"])


@router.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "PROJECT_DOMAIN": settings.PROJECT_DOMAIN}
    )
