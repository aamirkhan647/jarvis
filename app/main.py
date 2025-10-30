import streamlit as st
from core.orchestrator import Orchestrator
from tools.resume_parser import (
    parse_resume,
    get_mock_resume_text,
)  # Using mock resume for easy testing

st.set_page_config(page_title="Agentic Job Tailor", layout="wide")

# Initialize Session State
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = Orchestrator()
if "jobs_found" not in st.session_state:
    st.session_state.jobs_found = []
if "base_resume_text" not in st.session_state:
    st.session_state.base_resume_text = get_mock_resume_text()  # Start with mock text
if "selected_job" not in st.session_state:
    st.session_state.selected_job = None
if "tailoring_results" not in st.session_state:
    st.session_state.tailoring_results = None


orchestrator = st.session_state.orchestrator

st.title("🤖 Agentic Job Search and Tailoring System")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("1. Resume Input")
    st.markdown("*(Using mock resume text for demonstration.)*")

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF/TXT/DOCX)", type=["pdf", "docx", "txt"]
    )
    if uploaded_file:
        st.session_state.base_resume_text = parse_resume(uploaded_file)
        st.success("Resume parsed successfully!")

    if st.session_state.base_resume_text:
        with st.expander("View Base Resume Text"):
            st.code(st.session_state.base_resume_text, language="text")

    st.header("2. Search Criteria")
    keywords = st.text_input("Keywords", "Agentic AI Engineer")
    location = st.text_input("Location", "Remote")

    if st.button("Start Job Search & Scoring"):
        if st.session_state.base_resume_text:
            st.session_state.tailoring_results = None  # Clear previous results
            with st.spinner("Agents are searching and analyzing jobs..."):
                results = orchestrator.run_initial_search(
                    keywords, location, st.session_state.base_resume_text
                )
                st.session_state.jobs_found = results
                st.success("Analysis complete!")
        else:
            st.error("Please provide resume text (upload or use mock).")

# --- Main Display Area (Job Results) ---

if st.session_state.jobs_found:
    st.header("3. Scored Job Results")

    # Sort by relevance score
    sorted_jobs = sorted(
        st.session_state.jobs_found, key=lambda x: x[1].relevance_score, reverse=True
    )

    for job, score in sorted_jobs:
        col1, col2 = st.columns([0.7, 0.3])

        with col1:
            st.subheader(f"{job.title} - {job.company}")
            st.caption(f"{job.location} | [View Job]({job.link})")

            # Display Scorecard details
            score_type = "Deep LLM" if score.is_llm_scored else "Keyword Match"
            st.markdown(
                f"**Relevance Score:** **{score.relevance_score}/100** *({score_type})*"
            )
            st.write(f"**Rationale:** {score.rationale}")
            st.write(f"**Key Matches:** {', '.join(score.matching_keywords)}")
            st.write(f"**Gaps:** {', '.join(score.gaps_identified)}")

        with col2:
            if st.button(f"Tailor Resume for {job.company}", key=job.link):
                st.session_state.selected_job = job

                with st.spinner(f"Tailoring and validating for {job.company}..."):
                    tailored_resume, ats_score = orchestrator.process_tailoring(
                        job, st.session_state.base_resume_text
                    )
                    st.session_state.tailoring_results = (tailored_resume, ats_score)
                st.experimental_rerun()  # Refresh to show results below

# --- Tailoring and Validation Step ---

if st.session_state.tailoring_results:
    tailored_resume, ats_score = st.session_state.tailoring_results
    job = st.session_state.selected_job

    st.divider()
    st.header(f"4. Final Tailoring & ATS Validation for: {job.title}")

    col_ats, col_rec = st.columns([0.4, 0.6])

    with col_ats:
        st.subheader("ATS Validation Score")
        st.metric(
            label="ATS Pass Confidence",
            value=f"{ats_score.ats_pass_confidence}%",
            delta_color="normal",
        )
        st.markdown(
            f"**Keyword Match:** {ats_score.keyword_match_score}%  | **Formatting:** {ats_score.formatting_hygiene}%"
        )

    with col_rec:
        st.subheader("Recommendations")
        st.warning(
            "Suggestions to improve ATS score: "
            + ", ".join(ats_score.recommendations_for_fix)
        )

    st.subheader("Tailored Resume Output (Draft)")
    st.code(tailored_resume, language="markdown")

    # Save option
    st.download_button(
        label=f"Download {job.company} Resume",
        data=tailored_resume,
        file_name=f"resume_tailored_for_{job.company.replace(' ', '_')}.txt",
        mime="text/plain",
    )
