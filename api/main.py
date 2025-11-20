from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

# 修正模板路径
BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR.parent / "app" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# 假设我们用一个简单的用户字典做测试
fake_users = {
    "test@example.com": "password123"
}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    user_password = fake_users.get(email)
    if not user_password or user_password != password:
        # 登录失败，显示错误
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid email or password"}
        )
    # 登录成功，跳转到 dashboard
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return response

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/category", response_class=HTMLResponse)
def category(request: Request):
    return templates.TemplateResponse("category.html", {"request": request})
