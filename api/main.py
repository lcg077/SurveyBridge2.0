from fastapi import FastAPI

app = FastAPI()

# ❌ 不要 static，因为你没有 static 文件夹
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return {"message": "backend running"}
