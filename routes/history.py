from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from database.database import SessionLocal
from models.daily_log import DailyLog

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/history")
def history_page(request: Request):
    db = SessionLocal()

    logs = db.query(DailyLog).order_by(DailyLog.id.desc()).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "logs": logs
        }
    )