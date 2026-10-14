from pydantic import BaseModel


class Create_Student(BaseModel):
    first_name : str
    last_name : str
    age : int
    ph_no : str
    email : str
    password : str


class Login_Student(BaseModel):
    email : str
    password : str


class Update_Student(BaseModel):
    id : int
    first_name : str
    last_name : str
    age : int
    ph_no : str
