from fastapi import FastAPI

from app.server.routes.routes import router

# Основная точка взаимодействия для создания всего API
app = FastAPI()

# Подключение роутеров к точке взаимодействия
app.include_router(router, tags=["Notification"])
