from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 你原来 app 的代码（core.py）可以这样导入
from core import router

app = FastAPI()

# 连接路由
app.include_router(router)

# 在 Vercel 上要手动挂载 static 文件夹
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/api/health")
def health():
    return {"status": "ok"}
