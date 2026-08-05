from app.routes.execute import router
from fastapi import FastAPI

app = FastAPI(
    title="WasmBox Backend API",
    description="Secure Python Code Execution Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to WasmBox Backend 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
app.include_router(router)