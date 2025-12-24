from fastapi import FastAPI, Request, Form, Depends, HTTPException, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import engine, Base, get_db
from app.models import User, Survey

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)

# ---------------------------
# 首页
# ---------------------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "show": None, "error": None}
    )

# ---------------------------
# 登录
# ---------------------------
@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        return templates.TemplateResponse(
            "index.html",
            {"request": {}, "show": "login", "error": "Invalid email or password"}
        )

    response = RedirectResponse("/choice", status_code=303)
    response.set_cookie("user_id", str(user.id))
    return response

# ---------------------------
# 注册
# ---------------------------
@app.post("/register")
def register(
    email: str = Form(...),
    password: str = Form(...),
    confirm: str = Form(...),
    db: Session = Depends(get_db)
):
    if password != confirm:
        return templates.TemplateResponse(
            "index.html",
            {"request": {}, "show": "register", "error": "Passwords do not match"}
        )

    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse(
            "index.html",
            {"request": {}, "show": "register", "error": "Email already exists"}
        )

    user = User(
        email=email,
        password=pwd_context.hash(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("user_id", str(user.id))
    return response

# ---------------------------
# 当前用户
# ---------------------------
def get_current_user(
    user_id: str = Cookie(None),
    db: Session = Depends(get_db)
):
    if not user_id:
        raise HTTPException(401, "Not logged in")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(401, "User not found")
    return user

# ---------------------------
# 选择页
# ---------------------------
@app.get("/choice", response_class=HTMLResponse)
def choice(request: Request):
    return templates.TemplateResponse("choice.html", {"request": request})

@app.get("/publisher", response_class=HTMLResponse)

def publisher_dashboard(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    surveys = (
        db.query(Survey)
        .filter(Survey.publisher_id == current_user.id)
        .all()
    )

    return templates.TemplateResponse(
        "publisher.html",
        {
            "request": request,
            "surveys": surveys
        }
    )
@app.post("/publisher/delete/{survey_id}")
def delete_survey(
    survey_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    survey = (
        db.query(Survey)
        .filter(
            Survey.id == survey_id,
            Survey.publisher_id == current_user.id
        )
        .first()
    )

    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    db.delete(survey)
    db.commit()

    return RedirectResponse(url="/publisher", status_code=303)

# ---------------------------
# Browse === Dashboard（重定向）
# ---------------------------
@app.get("/browse")
def browse_redirect():
    return RedirectResponse("/dashboard", status_code=302)

# ---------------------------
# Dashboard（全平台 survey）
# ---------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    surveys = db.query(Survey).all()

    surveys_data = [
        {
            "id": s.id,
            "title": s.title,
            "desc": s.description,
            "link": s.form_url,
            "category": s.category,
            "time": f"{s.estimated_time} min",
            "reward": f"${s.reward_amount}",
            "responses": f"{s.current_responses}/{s.target_responses}",
            "img": "/static/default.jpg"
        }
        for s in surveys
    ]

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "surveys": surveys_data
        }
    )

# ---------------------------
# 发布页面
# ---------------------------
@app.get("/publish", response_class=HTMLResponse)
def publish_page(request: Request):
    return templates.TemplateResponse("publish.html", {"request": request})

# ---------------------------
# 发布 survey
# ---------------------------
@app.post("/publish")
def publish_survey(
    title: str = Form(...),
    description: str = Form(...),
    form_url: str = Form(...),
    category: str = Form(...),
    estimated_time: int = Form(...),
    reward_amount: float = Form(...),
    target_responses: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    survey = Survey(
        publisher_id=current_user.id,
        title=title,
        description=description,
        form_url=form_url,
        category=category,
        estimated_time=estimated_time,
        reward_amount=reward_amount,
        target_responses=target_responses,
        current_responses=0
    )
    db.add(survey)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)
