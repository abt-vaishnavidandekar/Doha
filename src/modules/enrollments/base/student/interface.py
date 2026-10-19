from pydantic import BaseModel


class Create_Enrollment(BaseModel):
    student_id : int
    course_id : int
    batch_id : int


class Check_seats(BaseModel):
    batch_id : int