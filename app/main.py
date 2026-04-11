from fastapi import FastAPI

from app.routes import recommend,ingest

app = FastAPI()

@app.get("/")
def health_check():
    return "Hello From Server"

app.include_router(ingest.router)
app.include_router(recommend.router)
