from fastapi import FastAPI

from app.routes.recommend import router

app = FastAPI()

@app.get("/")
def health_check():
    return "Hello From Server"

app.include_router(router)
