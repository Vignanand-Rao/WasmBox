from fastapi import APIRouter, HTTPException
from app.models.request import CodeRequest
from app.services.execution_service import execute_code

router = APIRouter()

@router.post(
    "/execute",
    tags=["Execution"],
    summary="Execute user code securely"
)
def execute(request: CodeRequest):
    try:
        return execute_code(request.code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))