from pydantic import BaseModel


class Create_Batch(BaseModel):
    batch_name : str
    date_field : str
    starting_time : str
    ending_time : str
    seats : int
    course_id : int


class Update_Batch(BaseModel):
    batch_name : str | None = None
    date_field : str | None = None
    starting_time : str | None = None
    ending_time : str | None = None
    seats : int | None = None
    course_id : int | None = None