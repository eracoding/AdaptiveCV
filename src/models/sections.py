from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class AchievementList(BaseModel):
    achievements: List[str] = Field(
        description="Key accomplishments, honors, or milestones that highlight professional capability and relevance to the job role."
    )

class Credential(BaseModel):
    title: str = Field(description="Certification title.")
    issuer: str = Field(description="Organization that granted the certification.")
    url: str = Field(description="Verification link for the certification.")

class CredentialList(BaseModel):
    certifications: List[Credential] = Field(
        description="Professional certifications with issuer name and verification links."
    )

class AcademicRecord(BaseModel):
    degree: str = Field(description="Full degree title, including major. e.g., MSc in Artificial Intelligence.")
    institution: str = Field(description="Name and location of the institution. e.g., MIT, Cambridge, USA.")
    start: str = Field(description="Start date of the academic period. Format: e.g., Sep 2021.")
    end: str = Field(description="End date of the academic period. Format: e.g., May 2023.")
    coursework: List[str] = Field(description="Relevant subjects or modules completed.")

class AcademicHistory(BaseModel):
    education: List[AcademicRecord] = Field(
        description="Educational background, including degrees, institutions, duration, and key subjects."
    )

class ReferenceLink(BaseModel):
    label: str = Field(description="Label or description of the resource.")
    url: str = Field(description="The link to the external resource or document.")

class PortfolioProject(BaseModel):
    title: str = Field(description="Title of the project.")
    category: Optional[str] = Field(description="Classification, e.g., hackathon, course project, or research.")
    repo_url: str = Field(description="Repository or live demo link.")
    resources: Optional[List[ReferenceLink]] = Field(description="Related assets such as videos, presentations, or documentation.")
    start: str = Field(description="Project start date. e.g., Jan 2022.")
    end: str = Field(description="Project end date. e.g., Mar 2022.")
    highlights: List[str] = Field(
        description="Three concise bullet points explaining impact and results using action verbs, numbers, and STAR method."
    )

class ProjectPortfolio(BaseModel):
    projects: List[PortfolioProject] = Field(
        description="Detailed list of completed projects, including metadata and achievements."
    )

class SkillGroup(BaseModel):
    title: str = Field(description="Skill area title such as Programming Languages, Cloud Platforms, or Soft Skills.")
    items: List[str] = Field(description="List of tools or competencies in the category.")

class SkillMatrix(BaseModel):
    skill_section: List[SkillGroup] = Field(
        description="Collection of categorized skills relevant to the candidate’s profile."
    )

class JobExperience(BaseModel):
    position: str = Field(description="Job title. e.g., Backend Developer.")
    employer: str = Field(description="Name of the organization.")
    location: str = Field(description="Company location. e.g., Berlin, Germany.")
    start: str = Field(description="Start date of employment.")
    end: str = Field(description="End date of employment.")
    contributions: List[str] = Field(
        description="Three bullet points describing role-specific accomplishments and tasks using quantifiable metrics and active language."
    )

class WorkHistory(BaseModel):
    work_experience: List[JobExperience] = Field(
        description="Summary of prior roles, including responsibilities and achievements."
    )

class SocialMedia(BaseModel):
    linkedin: Optional[HttpUrl] = Field(description="URL of LinkedIn profile.")
    github: Optional[HttpUrl] = Field(description="URL of GitHub account.")
    medium: Optional[HttpUrl] = Field(description="URL of Medium blog.")
    devpost: Optional[HttpUrl] = Field(description="URL of Devpost profile.")

class Resume(BaseModel):
    full_name: str = Field(description="Candidate’s full name.")
    summary: Optional[str] = Field(description="A short introduction or objective statement.")
    contact_number: str = Field(description="Phone number for contact.")
    email_address: str = Field(description="Primary email address.")
    media_profiles: SocialMedia = Field(description="Social media links for professional visibility.")
    work_experience: List[JobExperience] = Field(description="Work experience history with details.")
    education: List[AcademicRecord] = Field(description="Educational background with institutions and coursework.")
    skill_section: List[SkillGroup] = Field(description="Categorized list of relevant skills.")
    projects: List[PortfolioProject] = Field(description="Projects undertaken by the candidate.")
    certifications: List[Credential] = Field(description="Verified certifications.")
    achievements: List[str] = Field(description="Career highlights, awards, or recognitions.")
