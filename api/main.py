# api/main.py  ← Vercel 会自动运行这个文件

import sys
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 让 Vercel 找到你的 app/ 文件夹
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.core import router as core_router  # ← 关键


app = FastAPI()

# 挂载静态资源
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 模板位置
templates = Jinja2Templates(directory="app/templates")

# 挂载你所有的路由
app.include_router(core_router)
