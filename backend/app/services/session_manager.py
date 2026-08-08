import logging
import uuid
from datetime import datetime, timedelta, timezone


logger = logging.getLogger(__name__)

SESSION_TIMEOUT_MINUTES = 30

_sessions = {}


def _cleanup_expired_sessions() -> None:
    """Remove sessions that have been inactive for too long."""

    now = datetime.now(timezone.utc)

    expired_sessions = [
        session_id
        for session_id, session in _sessions.items()
        if now - session["last_activity"] > timedelta(
            minutes=SESSION_TIMEOUT_MINUTES
        )
    ]

    for session_id in expired_sessions:
        del _sessions[session_id]
        logger.info("Removed expired session: %s", session_id)


def create_session() -> str:
    """Create and register a new execution session."""

    _cleanup_expired_sessions()

    session_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    _sessions[session_id] = {
        "created_at": now,
        "last_activity": now,
        "request_count": 0
    }

    logger.info("Created execution session: %s", session_id)

    return session_id


def record_request(session_id: str) -> None:
    """Record an execution request for an existing session."""

    _cleanup_expired_sessions()

    if session_id not in _sessions:
        raise ValueError("Invalid or expired session ID")

    _sessions[session_id]["request_count"] += 1
    _sessions[session_id]["last_activity"] = datetime.now(timezone.utc)


def session_exists(session_id: str) -> bool:
    """Check whether a session exists and has not expired."""

    _cleanup_expired_sessions()

    return session_id in _sessions