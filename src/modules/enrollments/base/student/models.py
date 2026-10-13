from sqlalchemy import String, Integer, Boolean, func, DateTime, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.configs.model import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id : Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement=True)
    student_id : Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    course_id : Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    active_at : Mapped[bool] = mapped_column(Boolean, default=True)

    student = relationship("Student", back_populates="enrollment")
    batch = relationship("Batch", back_populates="enrollment")
    course = relationship("Course", back_populates="enrollment")
    