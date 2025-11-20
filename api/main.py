from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent

# 模板
templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")

# 静态文件
app.mount("/static", StaticFiles(directory=BASE_DIR / "app" / "static"), name="static")

# 模拟用户数据库
fake_users_db = {
    "test@example.com": "password123"
}

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "show": None, "error": None}
    )

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if email in fake_users_db and fake_users_db[email] == password:
        return RedirectResponse(url="/dashboard", status_code=303)
    else:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "show": "login", "error": "Invalid email or password."}
        )

@app.post("/register", response_class=HTMLResponse)
def register(request: Request, email: str = Form(...), password: str = Form(...), confirm: str = Form(...)):
    if email in fake_users_db:
        error = "Email already registered."
    elif password != confirm:
        error = "Passwords do not match."
    else:
        fake_users_db[email] = password
        # 注册成功跳回 login 弹窗
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "show": "login", "error": "Registration successful! Please login."}
        )
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "show": "register", "error": error}
    )

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )
