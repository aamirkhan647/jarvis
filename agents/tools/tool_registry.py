"""Tool registry exposes functions agents can call."""

from agents.tools import (
    scraping_tools,
    parsing_tools,
    embedding_tools,
    nlp_tools,
    tailoring_tools,
    ats_tools,
    research_tools,
    llm_tools,
)


def get_tool_registry():
    return {
        "search_jobs": scraping_tools.search_jobs,
        "parse_resume": parsing_tools.parse_resume,
        "embed_text": embedding_tools.embed_text,
        "score_similarity": embedding_tools.score_similarity,
        "extract_keywords": nlp_tools.extract_keywords,
        "tailor_resume": tailoring_tools.tailor_resume,
        "simulate_ats": ats_tools.simulate_ats,
        "research_company": research_tools.research_company,
        "llm_call": llm_tools.llm_call,
    }
