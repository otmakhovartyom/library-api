#!/usr/bin/python3

from pydantic import BaseModel
from typing import Optional
from datetime import date

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    genre: str
    publication_date: date

class BookCreate(BookBase):
    author_id: int

class Book(BookBase):
    id: int
    # author: Author
    author: Optional[Author] = None
    
    class Config:
        orm_mode = True

class RatingBase(BaseModel):
    rating: float

class RatingCreate(RatingBase):
    book_id: int

class Rating(RatingBase):
    id: int
    user: User
    book: Book
    
    class Config:
        orm_mode = True
