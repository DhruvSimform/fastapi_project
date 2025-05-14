from fastapi_mail import FastMail, MessageSchema
from pydantic import EmailStr

from ..config.email_config import conf
from ..config.settings import settings
from .template_engine import templates


async def send_welcome_email(to_email: EmailStr, username: str):
    message = MessageSchema(
        subject=f"Welcome to FastAPI Project, {username}",
        recipients=[to_email],
        template_body={"username": username},
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email/welcome_email.html")
