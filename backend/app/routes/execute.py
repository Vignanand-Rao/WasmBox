import logging
import queue

from fastapi import APIRouter, HTTPException

from app.models.request import CodeRequest
from app.services.request_queue import submit_execution


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/execute",
    tags=["Execution"],
    summary="Execute user code securely"
)
def execute(request: CodeRequest):
    try:
        future = submit_execution(request.code)

    except queue.Full:
        logger.warning("Execution queue is full")

        raise HTTPException(
            status_code=503,
            detail="Execution queue is full. Please try again later."
        )

    try:
        return future.result()

    except Exception:
        logger.exception(
            "Unexpected error while processing queued execution request"
        )

        raise HTTPException(
            status_code=500,
            detail="Code execution failed due to an internal server error"
        )