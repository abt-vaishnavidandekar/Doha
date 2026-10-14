from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.configs.model import Base


class Student(Base):
    __tablename__ = "students"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name : Mapped[str] = mapped_column(String(50))
    last_name : Mapped[str] = mapped_column(String(50))
    age : Mapped[int] = mapped_column(Integer)
    ph_no : Mapped[str] = mapped_column(String(50))

    email : Mapped[str] = mapped_column(String(50))
    password : Mapped[str] = mapped_column(String)

    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    active_at : Mapped[bool] = mapped_column(Boolean, default=True)




    