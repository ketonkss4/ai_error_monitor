from pydantic.v1 import BaseModel, Field


class CorrectionsEval(BaseModel):
    needs_corrections: bool = Field(description="Whether the code needs corrections")
    corrections: str = Field(description="A full description of all the corrections that need to be made")
