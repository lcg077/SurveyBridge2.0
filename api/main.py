import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 让 Python 找到 app/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, "..", "app")
sys.path.append(APP_DIR)

from app.core import router as core_router

app = FastAPI()

# 如果你还没有静态文件，暂时不挂载
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 模板目录（必须存在）
templates = Jinja2Templates(directory="app/templates")

# 挂路由
app.include_router(core_router)
