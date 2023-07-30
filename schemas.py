from pydantic import BaseModel, EmailStr, Field
from datetime  import date

class ContactModel(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday:date
    notes:str


class ContactResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday:date
    notes:str
    
    class Config:
        orm_mode  = True
