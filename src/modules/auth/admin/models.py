from sqlalchemy import String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column
from src.configs.model import Base
from datetime import datetime


class Admin(Base):
    __tablename__ = "admins"

    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name : Mapped[str] = mapped_column(String(20))
    last_name : Mapped[str] = mapped_column(String(20))

    email : Mapped[str] = mapped_column(String(50))
    password : Mapped[str] = mapped_column(String)

    created_at : Mapped[datetime] = mapped_column(default=datetime.now, server_default=func.now())
    active_at : Mapped[bool] = mapped_column(Boolean, default=True)