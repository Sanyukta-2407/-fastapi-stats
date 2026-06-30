from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import uuid
import time

app = FastAPI()

# Allowed CORS origin
ALLOWED_ORIGIN = "https://dash-zk8zhh.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL = "22f2001139@ds.study.iitm.ac.in"


# Middleware to add required headers
@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    return response


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "FastAPI Stats Service is running"
    }


# Stats endpoint
@app.get("/stats")
def stats(values: str = Query(...)):
    nums = [int(x.strip()) for x in values.split(",")]

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }