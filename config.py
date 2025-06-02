import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY') or "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"
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL = "mistralai/mistral-7b-instruct:free"