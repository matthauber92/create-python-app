import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from core.schemas.base.base import Base


class User(Base):
  __tablename__ = "users"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  username = Column(String(255), unique=True)
  password = Column(String(100), unique=False)
  email = Column(String(255), unique=True)
