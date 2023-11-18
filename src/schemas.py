from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date


# post
class ContactModel(BaseModel):  

    name: str = Field(min_length=2, max_length=20)
    lastname: str = Field(min_length=2, max_length=20)
    email: str = EmailStr 
    phone: str = Field(min_length=5, max_length=20)
    birthday: date | None = None
    description: str = Field()
    age: int



 # get
class ContactResponse(BaseModel):
    id: int = 1
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    birthday: date | None
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    # у shemas подружить  models через class Config з orm базою даних
    class Config:
        from_attributes = True
        orm_mode = True



class ContactUpdate(BaseModel):
    email: EmailStr
    # phone: str
    name: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    description: Optional[str] = None
