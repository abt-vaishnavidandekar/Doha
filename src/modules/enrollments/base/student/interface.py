from pydantic import BaseModel


class Create_Enrollment(BaseModel):
    course_id : int
    student_id : int
    batch_id : int