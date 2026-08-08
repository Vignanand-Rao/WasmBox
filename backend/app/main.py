import logging

from app.routes.execute import router
from fastapi import FastAPI


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