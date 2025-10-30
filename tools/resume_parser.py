import streamlit as st


def parse_resume(uploaded_file: st.runtime.uploaded_file_manager.UploadedFile) -> str:
    """
    MOCK: Parses a resume file into clean text.
    In production, this would use libraries like pdfminer.six or python-docx.
    """
    if uploaded_file is None:
        return ""

    # Read as text for simplicity
    try:
        file_contents = uploaded_file.read().decode("utf-8")
        clean_text = file_contents.replace("\n", " ").strip()
        return clean_text
    except UnicodeDecodeError:
        return "Could not decode file. Please ensure it is plain text for this mock."


# Example mock content for testing the agents:
def get_mock_resume_text():
    return """
    John Smith - AI Engineer
    Summary: 5 years experience in software development. Strong background in Python.
    Skills: Python, Django, SQL, AWS, some ML concepts.
    Experience: 
      - Developed Python applications for data processing.
      - Worked with large datasets.
      - Led a small team of developers.
    """
