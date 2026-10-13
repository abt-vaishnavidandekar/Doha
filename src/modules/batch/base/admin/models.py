from sqlalchemy import String, Boolean, func, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.configs.model import Base
from datetime import datetime


class Batch(Base):
    __tablename__ = "batches"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date_field : Mapped[str] = mapped_column(String, nullable=False)
    starting_time : Mapped[str] = mapped_column(String)
    ending_time : Mapped[str] = mapped_column(String)

    student_id : Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    course_id : Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    active_at : Mapped[bool] = mapped_column(Boolean, default=True)

    enrollment = relationship("Enrollment", back_populates="batch")
    course = relationship("Course", back_populates="batch")
    student = relationship("Student", back_populates="batch")

