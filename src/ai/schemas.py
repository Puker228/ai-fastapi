from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    description: str


class Prompt(BaseModel):
    model: str = "gemma3:270m"
    prompt: str | None = "Why is the sky blue?"
    stream: bool | None = False
