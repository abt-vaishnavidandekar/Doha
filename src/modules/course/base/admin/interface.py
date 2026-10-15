from pydantic import BaseModel


class Create_Course(BaseModel):
    name : str
    description: str
    overview : str

class Course_Update(BaseModel):
    id : int
    name : str | None = None
    description: str | None = None
    overview : str | None = None
    document : str | None = None