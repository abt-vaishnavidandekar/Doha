from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.configs.model import Base


class Batch(Base):
    __tablename__ = "batches"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    batch_name : Mapped[str] = mapped_column(String)
    date_field : Mapped[str] = mapped_column(String, nullable=False)
    starting_time : Mapped[str] = mapped_column(String)
    ending_time : Mapped[str] = mapped_column(String)
    seats : Mapped[int] = mapped_column(Integer)

    course_id : Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    active_at : Mapped[bool] = mapped_column(Boolean, default=True)



