from pydantic import BaseModel, EmailStr, validator, ValidationError, Field
from datetime import datetime, date
from typing import Optional, List
# from pydantic.types import conint


class Book(BaseModel):
    id: int
    title: str
    isbn : int
    number_of_pages: int
    description: Optional[str] = None
    class Config:
        orm_mode = True

class AuthorsSchema(BaseModel):
    id: int 
    first_name: str 
    last_name: str
    birth_date: date 
    books :List[ Book]
    class Config:
        orm_mode = True

class Authors(BaseModel):
    id: int 
    first_name: str 
    last_name: str
    birth_date: date 
    
    class Config:
        orm_mode = True

# class AuthorsSchema(Schema):
#     id = fields.Integer(dump_only=True)
#     first_name = fields.String(required=True, validate=validate.Length(max=50))
#     last_name = fields.String(required=True, validate=validate.Length(max=50))
#     birth_date = fields.Date('%d-%m-%Y', required=True)
#     books = fields.List(fields.Nested(lambda: BookSchema(exclude=['author'])))


    # @validator("birth_date", allow_reuse=True)
    # def validate_birth_date(cls, value):
    #     if value > datetime.now().date():
    #         raise ValidationError(f"Birth date must by lower then {datetime.now().date()}")

    
class CreateAuthorSchema(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    class Config:
        orm_mode = True


class Books(BaseModel):
    id: int
    title: str
    isbn : int
    number_of_pages: int
    description: Optional[str] = None
    author_id: int
    author: Authors
    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    isbn : int
    number_of_pages: int
    description: Optional[str] = None
    class Config:
        orm_mode = True

class CreateBook(BaseModel):
    author_id: int
    title: str
    isbn: int
    number_of_pages: int
    description: Optional[str] = None
    class Config:
        orm_mode = True


class BookAut(BaseModel):
    author: CreateAuthorSchema
    book: CreateBook
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_tokes: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



class User(BaseModel):
    id:int
    username: str
    email: EmailStr
    creation_date: datetime
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    class Config:
        orm_mode = True

class UpdateUserData(BaseModel):
    username: str
    email: EmailStr
    class Config:
        orm_mode = True

class UpdateUserPassword(BaseModel):
    current_password: str
    new_password: str
    class Config:
        orm_mode = True