# 🏛️ Library Management API

REST API для управления библиотекой с системой рекомендаций книг. Реализовано на FastAPI с использованием SQLite.

## 📌 Возможности
- 🔐 Аутентификация по JWT-токенам
- 📚 CRUD-операции для книг, авторов и пользователей
- ⭐ Оценка книг пользователями
- 🧠 Персонализированные рекомендации книг
- 📊 Документация Swagger/ReDoc

## 🛠 Технологии
- Python 3.10+
- FastAPI
- SQLAlchemy (ORM)
- SQLite (можно переключить на PostgreSQL)
- JWT-аутентификация
- Pydantic (валидация данных)

## 🚀 Запуск проекта
1. Клонирование репозитория:
```bash
git clone https://github.com/ваш-репозиторий/library-api.git
cd library-api
```

2. Установка зависимостей:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

3. Запуск сервера:
```bash
uvicorn main:app --reload
```

Документация будет доступна:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🌐 Основные эндпоинты
| Метод | Путь                     | Описание                          |
|-------|--------------------------|-----------------------------------|
| POST  | /auth/token              | Получение JWT-токена              |
| GET   | /api/v1/books/           | Получить список книг              |
| POST  | /api/v1/books/           | Добавить новую книгу              |
| GET   | /api/v1/recommendations/ | Персонализированные рекомендации  |
| POST  | /api/v1/ratings/         | Оценить книгу                     |

## 🧪 Тестирование
```bash
pytest
```

## 📊 Структура проекта
```
library-api/
├── app
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── auth.py
│   ├── endpoints.py
│   ├── recommendations.py
│   └── database.py
├── test_main.py
├── requirements.txt
└── README.md
```

## ⚠️ Устранение неполадок
При ошибках:
1. Проверьте логи сервера
2. Убедитесь, что БД создана
3. Проверьте JWT-токен
