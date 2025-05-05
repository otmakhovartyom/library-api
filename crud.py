#!/usr/bin/python3

from sqlalchemy.orm import Session
import models, schemas
from auth import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_books(db: Session, skip: int = 0, limit: int = 100, genre: str = None, author_id: int = None):
    query = db.query(models.Book)
    
    # Применяем фильтры, если они переданы
    if genre:
        query = query.filter(models.Book.genre == genre)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    
    books = query.offset(skip).limit(limit).all()
    return books

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def create_rating(db: Session, rating: schemas.RatingCreate, user_id: int):
    db_rating = models.UserBookRating(**rating.dict(), user_id=user_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_ratings(db: Session, skip: int = 0, limit: int = 100, user_id: int = None, book_id: int = None):
    query = db.query(models.UserBookRating)
    
    # Применяем фильтры, если они переданы
    if user_id:
        query = query.filter(models.UserBookRating.user_id == user_id)
    if book_id:
        query = query.filter(models.UserBookRating.book_id == book_id)
    
    books = query.offset(skip).limit(limit).all()
    return books
