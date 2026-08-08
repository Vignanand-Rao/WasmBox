import logging
import queue

from fastapi import APIRouter, HTTPException

from app.models.request import CodeRequest
from app.models.response import CodeResponse
from app.services.request_queue import submit_execution
from app.services.session_manager import (
    create_session,
    record_request,
    session_exists,
)


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/execute",
    response_model=CodeResponse,
    tags=["Execution"],
    summary="Execute user code securely"
)
def execute(request: CodeRequest):
    # Create a new session if the client does not provide one.
    if request.session_id is None:
        session_id = create_session()
    else:
        session_id = request.session_id

        if not session_exists(session_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid session ID"
            )

    try:
        record_request(session_id)

        future = submit_execution(request.code)

    except queue.Full:
        logger.warning(
            "Execution queue is full for session %s",
            session_id
        )

        raise HTTPException(
            status_code=503,
            detail="Execution queue is full. Please try again later."
        )

    except Exception:
        logger.exception(
            "Failed to queue execution request for session %s",
            session_id
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to process execution request"
        )

    try:
        result = future.result()

        return {
            **result,
            "session_id": session_id
        }

    except Exception:
        logger.exception(
            "Unexpected error while processing queued request for session %s",
            session_id
        )

        raise HTTPException(
            status_code=500,
            detail="Code execution failed due to an internal server error"
        )