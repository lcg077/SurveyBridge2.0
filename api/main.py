from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import SessionLocal, engine, Base, get_db
from app.models import User

# 初始化 FastAPI 和模板
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 确保数据库建表
Base.metadata.create_all(bind=engine)

# 首页
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "show": None, "error": None}
    )

# 登录
@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if user and pwd_context.verify(password, user.password):
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "show": "login", "error": "Invalid email or password."}
    )

# 注册
@app.post("/register", response_class=HTMLResponse)
def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirm: str = Form(...),
    db: Session = Depends(get_db)
):
    if password != confirm:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "show": "register", "error": "Passwords do not match."}
        )
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "show": "register", "error": "Email already registered."}
        )

    hashed_password = pwd_context.hash(password)
    new_user = User(email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/dashboard", status_code=302)

# Dashboard
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )
