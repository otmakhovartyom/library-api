#!/usr/bin/python3

from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session

import models, schemas, auth
from database import get_db

router = APIRouter()

def recommend_books(db: Session, user_id: int, limit: int = 5) -> List[schemas.Book]:
    # Получаем оценки пользователя
    user_ratings = db.query(models.UserBookRating).filter(models.UserBookRating.user_id == user_id).all()
    
    if not user_ratings:
        # Если у пользователя нет оценок, рекомендуем популярные книги
        popular_books = (
            db.query(models.Book)
            .join(models.UserBookRating)
            .group_by(models.Book.id)
            .order_by(func.avg(models.UserBookRating.rating).desc())
            .limit(limit)
            .all()
        )
        return popular_books
    
    # Получаем любимые жанры пользователя
    favorite_genres = (
        db.query(models.Book.genre, func.avg(models.UserBookRating.rating).label("avg_rating"))
        .join(models.UserBookRating)
        .filter(models.UserBookRating.user_id == user_id)
        .group_by(models.Book.genre)
        .order_by(func.avg(models.UserBookRating.rating).desc())
        .limit(3)
        .all()
    )
    
    # Получаем любимых авторов пользователя
    favorite_authors = (
        db.query(models.Author.id, func.avg(models.UserBookRating.rating).label("avg_rating"))
        .join(models.Book, models.Book.author_id == models.Author.id)
        .join(models.UserBookRating)
        .filter(models.UserBookRating.user_id == user_id)
        .group_by(models.Author.id)
        .order_by(func.avg(models.UserBookRating.rating).desc())
        .limit(3)
        .all()
    )
    
    # Рекомендуем книги по любимым жанрам и авторам
    recommended_books = (
        db.query(models.Book)
        .filter(
            (models.Book.genre.in_([genre[0] for genre in favorite_genres])) |
            (models.Book.author_id.in_([author[0] for author in favorite_authors]))
        )
        .outerjoin(models.UserBookRating, models.UserBookRating.book_id == models.Book.id)
        .group_by(models.Book.id)
        .order_by(func.avg(models.UserBookRating.rating).desc())
        .limit(limit)
        .all()
    )
    
    return recommended_books

@router.get("/recommendations/", response_model=List[schemas.Book])
def get_recommendations(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    return recommend_books(db, current_user.id, limit)
