from pydantic import BaseModel

class Update_Student(BaseModel):

    id : int
    first_name : str | None = None
    last_name : str | None = None
    age : int | None = None
    ph_no : str | None = None
    