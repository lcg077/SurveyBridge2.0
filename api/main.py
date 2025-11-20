import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 找到 app 目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "..")
APP_DIR = os.path.join(ROOT_DIR, "app")

# 确保 Python 能 import app.*
sys.path.append(ROOT_DIR)

from app.core import router as core_router

app = FastAPI()

# static 目录路径 = app/static
STATIC_DIR = os.path.join(APP_DIR, "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# templates 路径 = app/templates
templates = Jinja2Templates(directory=os.path.join(APP_DIR, "templates"))

# 挂路由
app.include_router(core_router)
