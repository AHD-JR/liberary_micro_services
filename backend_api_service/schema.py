from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from bson import ObjectId


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v, field=None):  # Add the field argument
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)


class BookStatusEnum(str, Enum):
    available = "available"
    borrowed = "borrowed"

class CategoryEnum(str, Enum):
    novel = "novel"
    self_help = "self help"
    fiction = "fiction"
    romance = "romance"
    others = "others"

class BookRequestModel(BaseModel):
    title: str
    category: str
    publisher: str

class BookResponseModel(BaseModel):
    book_id: str
    title: str
    category: str
    publisher: str
    status: BookStatusEnum
    created_at: datetime

class UserResponseModel(BaseModel):
    email: str
    first_name: str
    last_name: str
    created_at: datetime

class BorrowBookSchema(BaseModel):
    email: str
    book_id: ObjectIdStr
    borrow_date: datetime = datetime.now()
    days: int

    class Config:
        allow_populate_by_field_name = True
        arbitrary_types_allowed = True

class BorrowBookRequestModel(BaseModel):
    email: str
    book_id: str
    days: int

    class Config:
        allow_populate_by_field_name = True
        arbitrary_types_allowed = True

class BorrowedBookResponseModel(BaseModel):
    book_title: str
    borrower_name: str
    return_date: datetime


