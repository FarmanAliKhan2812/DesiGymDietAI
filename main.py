from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from models.daily_log import DailyLog
from datetime import datetime
from routes.auth import router as auth_router
from routes.admin import router as admin_router
from routes.tracker import router as tracker_router
from routes.history import router as history_router
from routes.planner import router as planner_router
from routes.user import router as user_router


from database.database import SessionLocal
from models.food import Food

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="desi-gym-secret-key")

templates = Jinja2Templates(directory="templates")
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(tracker_router)
app.include_router(history_router)
app.include_router(planner_router)
app.include_router(user_router)