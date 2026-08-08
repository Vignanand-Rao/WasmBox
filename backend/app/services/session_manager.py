import logging
import uuid
from datetime import datetime, timezone


logger = logging.getLogger(__name__)

_sessions = {}


def create_session() -> str:
    """Create and register a new execution session."""

    session_id = str(uuid.uuid4())

    _sessions[session_id] = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "request_count": 0
    }

    logger.info("Created execution session: %s", session_id)

    return session_id


def record_request(session_id: str) -> None:
    """Record an execution request for an existing session."""

    if session_id not in _sessions:
        raise ValueError("Invalid session ID")

    _sessions[session_id]["request_count"] += 1


def session_exists(session_id: str) -> bool:
    """Check whether a session exists."""

    return session_id in _sessions