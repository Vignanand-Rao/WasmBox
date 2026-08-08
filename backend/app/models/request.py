from pydantic import BaseModel, Field, field_validator


class CodeRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        max_length=100_000,
        description="Python source code to execute"
    )
    language: str = Field(
        default="python",
        description="Programming language"
    )

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Code cannot be empty or whitespace only")
        return value

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        value = value.strip().lower()

        if value != "python":
            raise ValueError("Only Python is currently supported")

        return value