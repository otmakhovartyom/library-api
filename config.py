#!/usr/bin/python3

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,  HTTPBearer

# Настройки приложения
SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Настройка аутентификации
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scheme_name="Bearer")
security = HTTPBearer()  # Используем простую Bearer-аутентификацию
