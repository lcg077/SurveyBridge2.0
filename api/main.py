# api/main.py  ← Vercel 会自动运行这个文件

import sys
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 获取项目根目录（绝对路径）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 让 Python 正确找到 app 包
sys.path.insert(0, BASE_DIR)

from app.core import router as core_router


app = FastAPI()

# 挂载静态资源（绝对路径）
static_path = os.path.join(BASE_DIR, "app/static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

# 模板目录（绝对路径）
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app/templates"))

# 挂载路由
app.include_router(core_router)
