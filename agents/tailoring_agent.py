from models.job_data import JobPost
from .base_agent import BaseAgent
from .prompts.system_prompts import TAILOR_PERSONA
import streamlit as st


class TailoringAgent(BaseAgent):
    def tailor_resume(self, job: JobPost, base_resume_text: str) -> str:
        """
        MOCK: Rewrites the base resume text using the job description keywords.
        """
        st.info(f"Tailoring resume draft for: {job.title}")

        # In production:
        # prompt = f"{TAILOR_PERSONA}\nJOB DESCRIPTION:\n{job.raw_description}\nBASE RESUME:\n{base_resume_text}"
        # tailored_text = self.llm.invoke(prompt).content

        # MOCK the tailored output
        target_keyword = job.raw_description.split(",")[0].strip()

        tailored_text = f"***TAILORED RESUME DRAFT (FOR {job.company})***\n\n"
        tailored_text += f"Summary: Highly proficient engineer with specific experience in {target_keyword}, aligning perfectly with {job.company}'s requirements.\n\n"
        tailored_text += "Experience:\n"
        tailored_text += f" - Architected and implemented solutions utilizing core principles of {target_keyword} to drive [business outcome].\n"
        tailored_text += " - Managed cloud infrastructure related to data pipelines (AWS/GCP expertise ensured).\n\n"
        tailored_text += "(...other sections refined for keyword density...)\n"

        return tailored_text
