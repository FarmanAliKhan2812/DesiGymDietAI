from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from database.database import SessionLocal
from models.food import Food

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate-plan")
def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    feet: int = Form(...),
    inches: int = Form(...),
    goal: str = Form(...)
):
    total_inches = (feet * 12) + inches
    height_cm = total_inches * 2.54
    height_m = height_cm / 100

    bmi = round(weight / (height_m ** 2), 2)

    if goal == "muscle_gain":
        protein_target = round(weight * 1.8)
        plan = [
            "Breakfast: 2 eggs + 2 roti + 1 glass milk",
            "Lunch: Chicken/daal + 2 roti + salad",
            "Snack: Banana + yogurt",
            "Dinner: Rice/roti + chicken/daal + vegetables"
        ]
    elif goal == "fat_loss":
        protein_target = round(weight * 1.6)
        plan = [
            "Breakfast: 2 boiled eggs + 1 roti",
            "Lunch: Daal/chicken + 1 roti + salad",
            "Snack: Fruit + green tea",
            "Dinner: Chicken/daal + vegetables, less rice"
        ]
    else:
        protein_target = round(weight * 1.3)
        plan = [
            "Breakfast: Egg + roti + milk",
            "Lunch: Normal home food with salad",
            "Snack: Fruit or yogurt",
            "Dinner: Balanced roti/rice + daal/chicken"
        ]

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "name": name,
            "age": age,
            "weight": weight,
            "feet": feet,
            "inches": inches,
            "height_cm": round(height_cm, 1),
            "goal": goal,
            "bmi": bmi,
            "protein_target": protein_target,
            "diet_plan": plan
        }
    )


@router.get("/plan-builder")
def plan_builder_page(request: Request, target: int = 135):
    db = SessionLocal()
    foods = db.query(Food).all()
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="plan_builder.html",
        context={
            "foods": foods,
            "target": target
        }
    )


@router.post("/plan-builder/generate")
async def generate_custom_plan(
    request: Request,
    protein_target: int = Form(...)
):
    form_data = await request.form()

    db = SessionLocal()
    foods = db.query(Food).all()
    db.close()

    selected_items = []
    total_protein = 0

    for food in foods:
        quantity = int(form_data.get(f"food_{food.id}", 0))

        if quantity > 0:
            food_total = quantity * food.protein
            total_protein += food_total

            selected_items.append({
                "name": food.name,
                "unit": food.unit,
                "quantity": quantity,
                "protein": food.protein,
                "total": food_total
            })

    remaining_protein = protein_target - total_protein

    if remaining_protein <= 0:
        status = "Your selected foods complete your protein target"
        remaining_protein = 0
    else:
        status = f"You still need {remaining_protein}g more protein"

    plan = []

    if len(selected_items) == 0:
        plan.append("No foods selected. Please enter quantity for at least one food.")
    else:
        for index, item in enumerate(selected_items):
            if index == 0:
                plan.append(f"Breakfast: {item['quantity']} x {item['name']} ({item['unit']})")
            elif index == 1:
                plan.append(f"Lunch: {item['quantity']} x {item['name']} ({item['unit']})")
            elif index == 2:
                plan.append(f"Snack: {item['quantity']} x {item['name']} ({item['unit']})")
            elif index == 3:
                plan.append(f"Dinner: {item['quantity']} x {item['name']} ({item['unit']})")
            else:
                plan.append(f"Extra option: {item['quantity']} x {item['name']} ({item['unit']})")

    return templates.TemplateResponse(
        request=request,
        name="custom_plan_result.html",
        context={
            "protein_target": protein_target,
            "selected_items": selected_items,
            "total_protein": total_protein,
            "remaining_protein": remaining_protein,
            "status": status,
            "plan": plan
        }
    )