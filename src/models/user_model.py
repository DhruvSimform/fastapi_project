import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String(length=50), unique=True)

    email = Column(String(length=50), unique=True)

    hash_password = Column(String)

    created_at = Column(DateTime, default=datetime.now())

    disable = Column(Boolean, default=False)

    def __repr__(self):
        return f"id: {self.id}, username: {self.username}"
