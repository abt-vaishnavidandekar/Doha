from pydantic import BaseModel


class Create_Course(BaseModel):
    name : str
    description: str
    overview : str