from pydantic import BaseModel, Field

class MovementAnalysis(BaseModel):
    answer: str
    contributing_factors: list[str] = Field(default_factory=list)
    supporting_evidence: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)