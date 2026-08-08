import logging

from fastapi import APIRouter, HTTPException
from app.models.request import CodeRequest
from app.services.execution_service import execute_code


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/execute",
    tags=["Execution"],
    summary="Execute user code securely"
)
def execute(request: CodeRequest):
    try:
        return execute_code(request.code)

    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error while processing code execution request")

        raise HTTPException(
            status_code=500,
            detail="Code execution failed due to an internal server error"
        )