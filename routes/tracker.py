from datetime import datetime

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from database.database import SessionLocal
from models.food import Food
from models.daily_log import DailyLog

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/tracker")
def tracker_page(request: Request, target: int = 135):
    db = SessionLocal()
    foods = db.query(Food).all()
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="tracker.html",
        context={
            "target": target,
            "foods": foods
        }
    )


@router.post("/track-protein")
async def track_protein(
    request: Request,
    protein_target: int = Form(...)
):
    form_data = await request.form()

    db = SessionLocal()
    foods = db.query(Food).all()

    protein_breakdown = {}
    total_protein = 0

    for food in foods:
        quantity = int(form_data.get(f"food_{food.id}", 0))
        food_total = quantity * food.protein

        protein_breakdown[f"{food.name} ({food.unit})"] = food_total
        total_protein += food_total

    db.close()

    remaining_protein = protein_target - total_protein

    progress = (total_protein / protein_target) * 100
    if progress > 100:
        progress = 100

    progress = round(progress, 1)

    if remaining_protein <= 0:
        status = "Daily protein target achieved"
        remaining_protein = 0
    else:
        status = f"You need {remaining_protein}g more protein today"

    return templates.TemplateResponse(
        request=request,
        name="tracker_result.html",
        context={
            "protein_breakdown": protein_breakdown,
            "total_protein": total_protein,
            "protein_target": protein_target,
            "remaining_protein": remaining_protein,
            "status": status,
            "progress": progress
        }
    )
@router.post("/save-log")
def save_log(
    request: Request,
    protein_target: int = Form(...),
    total_protein: int = Form(...),
    remaining_protein: int = Form(...)
):
    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/user-login",
            status_code=303
        )

    db = SessionLocal()

    log = DailyLog(
        user_id=request.session["user_id"],
        date=datetime.now().strftime("%d-%m-%Y"),
        protein_target=protein_target,
        total_protein=total_protein,
        remaining_protein=remaining_protein
    )

    db.add(log)
    db.commit()
    db.close()

    return RedirectResponse(
        url="/history",
        status_code=303
    )