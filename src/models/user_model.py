import uuid
from ..config.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import String , Column , DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(UUID( as_uuid=True),
                 primary_key=True,
                 default=uuid.uuid4)
    
    username = Column(String(length=50),
                      unique=True)
    
    email = Column( String(length=50),
                   unique=True)
    
    hash_passowrd = Column(String)

    created_at = Column(DateTime, default=datetime.now())


    def __repr__(self):
        return f"id: {self.id}, username: {self.username}"
    



