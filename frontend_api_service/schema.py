from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class BookStatusEnum(str, Enum):
    available = "avaiable"
    borrowed = "borrowed"

class BookRequestModel(BaseModel):
    title: str
    category: str
    publisher: str
    created_at: datetime = datetime.now()

class BookResponseModel(BaseModel):
    id: str
    title: str
    category: str
    publisher: str
    status: BookStatusEnum = BookStatusEnum.available
    created_at: datetime

    class Config:
        orm_mode = True

class UserRequestModel(BaseModel):
    email: str
    first_name: str
    last_name: str

class UserResponseModel(BaseModel):
    email: str
    first_name: str
    last_name: str
    created_at: datetime

    class Config:
        orm_mode = True

class BorrowRequestModel(BaseModel):
    email: str
    book_id: str
    days: int

class BorrowResponseModel(BaseModel):
    user_email: str
    book_id: str
    borrow_date: datetime
    number_of_days: int

    class Config:
        orm_mode = True


