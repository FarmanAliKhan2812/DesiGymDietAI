from urllib import request

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from database.database import SessionLocal
from models.daily_log import DailyLog

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/history")
def history_page(request: Request):

    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/user-login",
            status_code=303
        )

    db = SessionLocal()

    logs = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == request.session["user_id"])
        .order_by(DailyLog.id.desc())
        .all()
    )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "logs": logs
        }
    )