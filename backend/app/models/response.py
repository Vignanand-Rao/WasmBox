from pydantic import BaseModel

class CodeResponse(BaseModel):
    status: str
    output: str
    execution_time: float
    memory_usage: float