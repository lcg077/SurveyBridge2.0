import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# 让 Python 找到 app/
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.core import router as core_router

app = FastAPI()

# 自动根据 main.py 的位置挂载 static
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# 挂载路由
app.include_router(core_router)
