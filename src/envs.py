'''
---------------------------------
File: envs.py
Author: Ulugbek Shernazarov
Email: u.shernaz4rov@gmail.com
Copyright (c) 2025 Ulugbek Shernazarov. All rights reserved | GitHub: eracoding
---------------------------------
'''
from typing import Dict, Any, List

from src.prompts.sections_prompt import (
    EXPERIENCE,
    SKILLS,
    PROJECTS,
    EDUCATIONS,
    CERTIFICATIONS,
    ACHIEVEMENTS
)

from src.models.sections import (
    WorkHistory,
    SkillMatrix,
    ProjectPortfolio,
    AcademicHistory,
    CredentialList,
    AchievementList
)


class EmbeddingModels:
    """Constants for embedding models"""
    GPT = "text-embedding-ada-002" # Alternatives: text-embedding-3-large, text-embedding-3-small
    GEMINI = "models/text-embedding-004"  # Alternative: models/embedding-001
    OLLAMA = "bge-m3"


# Export individual model constants for backward compatibility
GPT_EMBEDDING_MODEL = EmbeddingModels.GPT
# GEMINI_EMBEDDING_MODEL = EmbeddingModels.GEMINI
# OLLAMA_EMBEDDING_MODEL = EmbeddingModels.OLLAMA

# Default LLM settings
DEFAULT_LLM_PROVIDER = "GPT"
DEFAULT_LLM_MODEL = "gpt-4o"

# LLM provider configuration
LLM_MAPPING: Dict[str, Dict[str, Any]] = {
    'GPT': {
        "api_env": "OPENAI_API_KEY",
        "model": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo", 
            "gpt-4-1106-preview", 
            "gpt-3.5-turbo"
        ],
    },
    # 'Gemini': {
    #     "api_env": "GEMINI_API_KEY",
    #     "model": [
    #         "gemini-1.5-flash", 
    #         "gemini-1.5-flash-latest", 
    #         "gemini-1.5-pro", 
    #         "gemini-1.5-pro-latest", 
    #         "gemini-1.5-pro-exp-0801"
    #     ],
    # },
}

# Resume section configuration mapping
section_mapping: Dict[str, Dict[str, Any]] = {
    "work_experience": {"prompt": EXPERIENCE, "schema": WorkHistory},
    "skill_section": {"prompt": SKILLS, "schema": SkillMatrix},
    "projects": {"prompt": PROJECTS, "schema": ProjectPortfolio},
    "education": {"prompt": EDUCATIONS, "schema": AcademicHistory},
    "certifications": {"prompt": CERTIFICATIONS, "schema": CredentialList},
    "achievements": {"prompt": ACHIEVEMENTS, "schema": AchievementList},
}
