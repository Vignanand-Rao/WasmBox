from fastapi import APIRouter
from app.models.request import CodeRequest
from app.services.execution_service import execute_code

router = APIRouter()

@router.post("/execute")
def execute(request: CodeRequest):
    result = execute_code(request.code)
    return result