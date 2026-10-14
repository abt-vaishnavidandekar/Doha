from pydantic import BaseModel


class Create_Admin(BaseModel):
    first_name : str
    last_name : str
    email : str
    password : str

class Admin_login(BaseModel):
    email : str
    password : str


class RefreshRequest(BaseModel):
    refresh_token: str