#!/usr/bin/python3

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# Импорт всех необходимых модулей
from models import Base
from endpoints import router as api_router
from recommendations import router as recommendations_router
from database import engine, get_db, Base

# Инициализация FastAPI
app = FastAPI(
    title="Library Management API",
    description="API for managing library with book recommendations",
    version="1.0.0"
)

# Создание таблиц при старте
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# Подключение всех роутеров
app.include_router(api_router, prefix="/api/v1", tags=["API"])
app.include_router(recommendations_router, prefix="/api/v1", tags=["Recommendations"])

# Базовый эндпоинт для проверки работы
@app.get("/", tags=["Status"])
def read_root():
    return {"status": "OK", "message": "Library API is running"}

# Эндпоинт для проверки соединения с БД
@app.get("/healthcheck", tags=["Status"])
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"database": "OK"}
    except Exception as e:
        return {"database": "Error", "details": str(e)}
