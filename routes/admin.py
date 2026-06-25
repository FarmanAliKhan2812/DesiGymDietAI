from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from database.database import SessionLocal
from models.food import Food

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/admin")
def admin_page(request: Request):
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/login", status_code=303)

    db = SessionLocal()
    foods = db.query(Food).all()
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={"foods": foods}
    )


@router.post("/admin/add-food")
def add_food(
    request: Request,
    name: str = Form(...),
    unit: str = Form(...),
    protein: int = Form(...)
):
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/login", status_code=303)

    db = SessionLocal()

    new_food = Food(name=name, unit=unit, protein=protein)

    db.add(new_food)
    db.commit()
    db.close()

    return RedirectResponse(url="/admin", status_code=303)


@router.post("/admin/delete-food/{food_id}")
def delete_food(request: Request, food_id: int):
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/login", status_code=303)

    db = SessionLocal()

    food = db.query(Food).filter(Food.id == food_id).first()

    if food:
        db.delete(food)
        db.commit()

    db.close()

    return RedirectResponse(url="/admin", status_code=303)


@router.get("/admin/edit-food/{food_id}")
def edit_food_page(request: Request, food_id: int):
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/login", status_code=303)

    db = SessionLocal()
    food = db.query(Food).filter(Food.id == food_id).first()
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="edit_food.html",
        context={"food": food}
    )


@router.post("/admin/update-food/{food_id}")
def update_food(
    request: Request,
    food_id: int,
    name: str = Form(...),
    unit: str = Form(...),
    protein: int = Form(...)
):
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/login", status_code=303)

    db = SessionLocal()

    food = db.query(Food).filter(Food.id == food_id).first()

    if food:
        food.name = name
        food.unit = unit
        food.protein = protein
        db.commit()

    db.close()

    return RedirectResponse(url="/admin", status_code=303)