from pydantic import BaseModel

class Create_Admin(BaseModel):
    first_name : str
    last_name : str
    email : str
    password : str

class Admin_login(BaseModel):
    email : str
    password : str

class Update_Admin(BaseModel):
    id : int | None = None
    first_name : str | None = None
    last_name : str | None = None