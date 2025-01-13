import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("sqlite:///summaries.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
