from setuptools import setup, find_packages

setup(
    name="ai-meeting-summarizer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "python-multipart",
        "whisper",
        "torch",
        "transformers",
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client"
    ],
) 