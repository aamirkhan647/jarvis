from pydantic import BaseModel, Field
from typing import List


class JobPost(BaseModel):
    title: str = Field(description="The job title.")
    company: str = Field(description="The hiring company.")
    location: str
    link: str
    raw_description: str = Field(description="The full text of the job description.")


class Scorecard(BaseModel):
    relevance_score: int = Field(description="Overall match score from 0 to 100.")
    rationale: str = Field(description="Brief explanation of the score.")
    matching_keywords: List[str] = Field(
        description="Keywords found in both resume and JD."
    )
    gaps_identified: List[str] = Field(
        description="Key skills missing from the resume."
    )
    is_llm_scored: bool = Field(description="True if deep LLM analysis was performed.")


class ATSScorecard(BaseModel):
    keyword_match_score: int
    formatting_hygiene: int
    keyword_density: int
    ats_pass_confidence: int = Field(
        description="Final overall confidence score 0-100."
    )
    recommendations_for_fix: List[str]
