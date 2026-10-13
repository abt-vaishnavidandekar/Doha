from sqlalchemy import String, Boolean, func, DateTime, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.configs.model import Base
from datetime import datetime


class Course(Base):
    __tablename__ = "courses"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(50))
    description : Mapped[str] = mapped_column(String(200))
    overview : Mapped[str] = mapped_column(String(750))
    
    created_at : Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(), server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    active_at : Mapped[bool] = mapped_column(Boolean, default=True)


    