import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String , func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from ..config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

    username = Column(String(length=50), unique=True, nullable=False)

    email = Column(String(length=50), unique=True, nullable=False)

    first_name = Column(String(length=50), nullable=True)

    last_name = Column(String(length=50), nullable=True)

    hash_password = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)

    disable = Column(Boolean, default=False, nullable=False)

    role = Column(String(length=20), default="user", nullable=False)
    bio = Column(String(length=255), nullable=True)
    profile_picture_url = Column(String, nullable=True)
    last_login = Column(DateTime, nullable=True)

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @full_name.expression
    def full_name(cls):
        return func.concat(cls.first_name, " ", cls.last_name)

    def __repr__(self):
        return f"<User id={self.id}, username={self.username}>"
    

