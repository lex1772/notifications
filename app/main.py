import os

import uvicorn
from dotenv import load_dotenv, find_dotenv

# Загрузка файла .env с автоматическим поиском
load_dotenv(find_dotenv())

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=int(os.getenv("PORT")), reload=True)
