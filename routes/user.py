from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services.auth_service import hash_password, verify_password

from database.database import SessionLocal
from models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={}
    )


@router.post("/signup")
def signup(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        db.close()
        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context={
                "error": "Email already exists."
            }
        )

    new_user = User(
        name=name,
        email=email,
        password_hash=hash_password(password)
    )

    db.add(new_user)
    db.commit()
    db.close()

    return RedirectResponse(
        url="/user-login",
        status_code=303
    )
@router.get("/user-login")
def user_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="user_login.html",
        context={}
    )


@router.post("/user-login")
def user_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        db.close()
        return templates.TemplateResponse(
            request=request,
            name="user_login.html",
            context={"error": "Invalid email or password"}
        )

    request.session["user_id"] = user.id
    request.session["user_name"] = user.name

    db.close()

    return RedirectResponse(
        url="/user-dashboard",
        status_code=303
    )


@router.get("/user-dashboard")
def user_dashboard(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(url="/user-login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="user_dashboard.html",
        context={
            "name": request.session.get("user_name")
        }
    )