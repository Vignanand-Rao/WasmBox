from typing import Optional

from pydantic import BaseModel


class CodeResponse(BaseModel):
    session_id: str
    status: str
    output: str
    errors: Optional[list[str]] = None
    execution_time: float
    memory_usage: float