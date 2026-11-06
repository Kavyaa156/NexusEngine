from pydantic import BaseModel, Field, field_validator

class QueryRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="The main text query for the AI engine."
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Controls randomness in AI output. Must be between 0.0 & 1.0."
    )
    max_tokens: int = Field(
        default=500,
        gt=0,
        description="Maximum length of the generated response"
    )

    @field_validator("prompt")
    @classmethod
    def validate_prompt_not_empty(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Prompt cannot be empty or consist only of whitespaces")
        return stripped