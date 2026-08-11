import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.execute import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

app = FastAPI(
    title="WasmBox Backend API",
    description="Secure Python Code Execution Platform",
    version="1.0.0",
    contact={
        "name": "WasmBox Team"
    },
    license_info={
        "name": "MIT"
    }
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Welcome to WasmBox Backend 🚀"
    }


@app.get(
    "/health",
    tags=["System"],
    summary="Backend Health Check"
)
def health():
    return {
        "status": "healthy",
        "service": "WasmBox Backend",
        "version": "1.0.0"
    }
app.include_router(router)