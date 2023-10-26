import os
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from dotenv import load_dotenv, find_dotenv
from fastapi import HTTPException
from starlette.responses import JSONResponse

from app.server.database import users_collection

# Загрузка файла .env с автоматическим поиском
load_dotenv(find_dotenv())


# Функция для поиска пользователя. Если пользователя нет, то создается тестовый пользователь
async def find_user(user_id):
    user = users_collection.find_one({"user_id": user_id})
    user_data = await user

    if user_data is not None:
        return user_data["email"]
    else:
        user = {"user_id": user_id, "email": os.getenv("EMAIL")}
        await users_collection.insert_one(user)
        return (await users_collection.find_one({"user_id": user_id}))["email"]


# Функция для отправыки письма на почту пользователю
async def send_mail(notification):
    try:
        msg = MIMEText(notification["key"], "html")
        msg['Subject'] = notification["key"]
        msg['From'] = f'{os.getenv("SMTP_NAME")} <{os.getenv("SMTP_EMAIL")}>'
        msg['To'] = str((await find_user(notification['user_id'])))

        server = SMTP_SSL(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")))
        server.login(os.getenv("SMTP_LOGIN"), os.getenv("SMTP_PASSWORD"))

        server.send_message(msg)
        server.quit()
        return JSONResponse({"success": True})

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
