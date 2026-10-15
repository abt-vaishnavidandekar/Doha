from pydantic import BaseModel


class Create_Batch(BaseModel):
    batch_name : str
    date_field : str
    start_date : str
    end_date : str
    ending_time : str
    seats : int
    course_id : int


class Update_Batch(BaseModel):
    id : int
    batch_name : str | None = None
    start_date : str | None = None
    end_date : str | None = None
    starting_time : str | None = None
    ending_time : str | None = None
    seats : int | None = None
    course_id : int | None = None