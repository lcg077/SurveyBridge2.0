from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

# 模板路径
BASE_DIR = Path(__file__).resolve().parent.parent  # api -> ../
templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")

# 模拟用户数据库
fake_users_db = {
    "test@example.com": "password123"
}

# 首页
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "show": None, "error": None}
    )

# 登录
@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if email in fake_users_db and fake_users_db[email] == password:
        # 登录成功跳转
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        # 登录失败显示错误
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "show": "login", "error": "Invalid email or password."}
        )

# 注册
@app.post("/register")
def register(request: Request, email: str = Form(...), password: str = Form(...), confirm: str = Form(...)):
    if email in fake_users_db:
        error = "Email already registered."
    elif password != confirm:
        error = "Passwords do not match."
    else:
        fake_users_db[email] = password
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "show": "register", "error": error}
    )

# Dashboard 页面
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )
