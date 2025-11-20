# api/main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# -------------------------------
# 首页
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# -------------------------------
# 登录
# -------------------------------
@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login", response_class=HTMLResponse)
def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    # 示例验证逻辑（可以替换成数据库验证）
    if email == "test@example.com" and password == "1234":
        return templates.TemplateResponse("dashboard.html", {"request": request, "user_email": email})
    else:
        error_msg = "Invalid email or password"
        return templates.TemplateResponse("login.html", {"request": request, "error": error_msg})

# -------------------------------
# 注册
# -------------------------------
@app.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})  # 如果你有 register.html 可换掉

# -------------------------------
# Dashboard
# -------------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    # 暂时不做登录验证，后面可以加 session/cookie
    return templates.TemplateResponse("dashboard.html", {"request": request, "user_email": "guest"})

# -------------------------------
# Category
# -------------------------------
@app.get("/category", response_class=HTMLResponse)
def category(request: Request):
    return templates.TemplateResponse("category.html", {"request": request})
