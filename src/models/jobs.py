from typing import List

from pydantic import BaseModel, Field

class JobData(BaseModel):
    title: str = Field(description="")
    goal: str = Field(description="")
    
    company_name: str = Field(description="")
    company_info: str = Field(description="")

    keywords: List[str] = Field(description="")
    duty_responsibility: List[str] = Field(description="")
    required_qualification: List[str] = Field(description="")
    preferred_qualification: List[str] = Field(description="")
