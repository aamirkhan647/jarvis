from setuptools import setup, find_packages

setup(
    name="jobtailor",
    version="0.1.0",
    author="Your Name",
    description="Agentic AI Job Search and Resume Tailoring System",
    packages=find_packages(),
    install_requires=[
        "tkinter",
        "requests",
        "beautifulsoup4",
        "lxml",
        "python-docx",
        "reportlab",
        "pandas",
        "numpy",
        "scikit-learn",
        "sentence-transformers",
        "faiss-cpu",
        "chroma",
        "openai",
        "tiktoken",
        "python-dotenv",
        "cryptography",
        "loguru",
    ],
    python_requires=">=3.9",
)
