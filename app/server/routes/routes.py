from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.server.database import (
    retrieve_notifications,
    create_notification,
    read_notification,
)
from app.server.models.models import (
    Notification,
)
from app.services import send_mail

router = APIRouter()


# Маршрут для создания уведомления
@router.post("/create", response_description="Notification data added into the database")
async def add(notification: Notification = Body(...)):
    notification = jsonable_encoder(notification)

    if notification["key"] == "registration":
        return await send_mail(notification)
    elif notification["key"] in ["new_message", "new_post"]:
        new_notification = await create_notification(notification)
        return JSONResponse(new_notification)
    elif notification["key"] == "new_login":
        await send_mail(notification)
        new_notification = await create_notification(notification)
        return JSONResponse(new_notification)
    return JSONResponse({"success": False})


# Маршрут для получения уведомлений
@router.get("/list", response_description="Notification data added into the database")
async def get(user_id: str, skip: int, limit: int):
    notifications = await retrieve_notifications(user_id, skip, limit)
    new = list(filter(lambda x: x['is_new'] is True, notifications))
    return JSONResponse({"success": True, "data": {"elements": len(notifications), "new": len(new),
                                                   "request": {"user_id": user_id, "skip": skip, "limit": limit},
                                                   "list": notifications}})


# Маршрут для прочтения уведомления
@router.post("/read", response_description="Notification data added into the database")
async def read(user_id: str, id: str):
    notification = await read_notification(user_id, id)
    return notification
