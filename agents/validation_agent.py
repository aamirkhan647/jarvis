from models.job_data import JobPost, ATSScorecard
from agents.base_agent import BaseAgent
from agents.prompts.system_prompts import ATS_PERSONA


class ValidationAgent(BaseAgent):
    def score_ats(self, job: JobPost, tailored_resume_text: str) -> ATSScorecard:
        """
        MOCK: Simulates an ATS parsing and scoring the tailored resume.
        """

        # In production, the LLM uses ATS_PERSONA and is forced into the ATSScorecard schema.

        # MOCK logic: high score if we successfully tailored the text
        if "Architected and implemented solutions" in tailored_resume_text:
            return ATSScorecard(
                keyword_match_score=95,
                formatting_hygiene=90,
                keyword_density=80,
                ats_pass_confidence=92,
                recommendations_for_fix=[
                    "Ensure date formatting is consistent (MM/YYYY)."
                ],
            )
        else:
            # Should not happen if TailoringAgent works, but serves as a low score example
            return ATSScorecard(
                keyword_match_score=40,
                formatting_hygiene=70,
                keyword_density=35,
                ats_pass_confidence=45,
                recommendations_for_fix=[
                    "Increase density of core technical skills found in the JD."
                ],
            )
