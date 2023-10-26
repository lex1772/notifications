from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


# Перечисление значений key
class KeyEnum(Enum):
    registration = 'registration'
    new_message = 'new_message'
    new_post = 'new_post'
    new_login = 'new_login'


# Класс для уведомлений пользователя
class Notification(BaseModel):
    timestamp: float = Field(default=datetime.now().timestamp())
    is_new: bool = Field(default=True)
    user_id: str = Field(..., min_length=24, max_length=24)
    key: KeyEnum
    target_id: str | None = Field(None, min_length=24, max_length=24)
    data: dict | None = Field(None)


# Класс для пользователя
class User(BaseModel):
    user_id: str = Field(..., min_length=24, max_length=24)
    email: EmailStr = Field(...)
    notifications: list[Notification] = []
