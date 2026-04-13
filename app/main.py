from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

from app.routes import recommend,ingest

app = FastAPI()

@app.get("/")
def health_check():
    return "Hello From Server"

app.include_router(ingest.router)
app.include_router(recommend.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("Error:", str(exc))

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc)
        }
    )