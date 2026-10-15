from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, DateTime, String, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.configs.model import Base


class Course(Base):
    __tablename__ = "courses"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(50))
    description : Mapped[str] = mapped_column(String(200))
    overview : Mapped[str] = mapped_column(String(750))
    document : Mapped[str] = mapped_column(String)
    
    created_at : Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(), server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    active_at : Mapped[bool] = mapped_column(Boolean, default=True)

