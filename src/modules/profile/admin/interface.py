from pydantic import BaseModel


class Update_Admin(BaseModel):
    id : int
    first_name : str | None = None
    last_name : str | None = None
    
