import os

import motor.motor_asyncio
from bson import ObjectId
from dotenv import load_dotenv, find_dotenv

# Загрузка файла .env с автоматическим поиском
load_dotenv(find_dotenv())

# Данные для соединения с базой данных
MONGO_DETAILS = os.getenv("DB_URI")

# Подключение к базе данных
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# Определяем базу данных
database = client.notifications

# Определяем коллекции базы данных
users_collection = database.get_collection("users_collection")

notifications_collection = database.get_collection("notifications_collection")


# Добавляем вспомогательные функции для анализа результатов запроса к базе данных в словарь
def user_helper(user) -> dict:
    return {
        "user_id": user["user_id"],
        "email": user["email"],
        "notifications": user["notifications"],
    }


def notification_helper(notification) -> dict:
    return {
        "id": str(notification["_id"]),
        "timestamp": notification["timestamp"],
        "is_new": notification["is_new"],
        "user_id": notification["user_id"],
        "key": notification["key"],
        "target_id": notification["target_id"],
        "data": notification["data"],
    }


# Получение списка уведомлений
async def retrieve_notifications(user_id: str, skip: int, limit: int):
    notifications = []
    async for notification in notifications_collection.find({"user_id": user_id}):
        notifications.append(notification_helper(notification))
    return notifications[skip:limit]


# Создание уведомления
async def create_notification(notification_data: dict) -> dict:
    notifications = []
    async for notification in notifications_collection.find({"user_id": notification_data['user_id']}):
        notifications.append(notification_helper(notification))
    if len(notifications) > 9:
        return {'error': "Уведомлений должно быть не больше 10"}
    await notifications_collection.insert_one(notification_data)
    return {"success": True}


# Прочтение уведомления
async def read_notification(user_id: str, id: str) -> dict:
    notification = await notifications_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if notification:
        updated_notification = await notifications_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"is_new": False}}
        )
        if updated_notification:
            return {"success": True}
        return {"success": False}
