"""
File: sections_prompt.py
"""
ACHIEVEMENTS = """
<task>
Generate a structured JSON 'achievements' resume section that highly aligns with the job description.
</task>

<input>
<achievements>
{section_data}
</achievements>

<job_description>
{job_description}
</job_description>
</input>

<guidelines>
- Prioritize maximum relevance to the job description, even if rephrasing or creative extrapolation is needed.
- You are allowed to adjust, transform, or invent plausible achievements that align with the user's background and the job description.
- Emphasize achievements showcasing the most relevant strengths, using active voice and flawless grammar.
</guidelines>

<example>
{{
  "achievements": [
    "Won E-yantra Robotics Competition 2018 - IITB.",
    "1st Prize in 'Prompt Engineering Hackathon 2023 for Humanities'.",
    "Awarded 'Extra Miller - 2021' at Winjit Technologies for exceptional contribution."
  ]
}}
</example>

{format_instructions}
"""

CERTIFICATIONS = """
<task>
Produce a JSON 'certifications' section highlighting credentials most relevant to the job post.
</task>

<input>
<certifications>
{section_data}
</certifications>

<job_description>
{job_description}
</job_description>
</input>

<guidelines>
- You must select or invent certifications that best match the skills, tools, or industry areas mentioned in the job description.
- Maintain naming consistency, plausible issuing authorities, and valid formatting of URLs.
- Creative extrapolation is allowed if necessary to align better.
</guidelines>

<example>
{{
  "certifications": [
    {{
      "title": "Deep Learning Specialization",
      "issuer": "DeepLearning.AI, Coursera Inc.",
      "url": "https://coursera.org/verify/xyz"
    }},
    {{
      "title": "Backend Development",
      "issuer": "HKUST",
      "url": "https://coursera.org/verify/abc"
    }}
  ]
}}
</example>

{format_instructions}
"""

EDUCATIONS = """
<task>
Create a JSON 'education' section from the user's academic history that best supports the job description.
</task>

<input>
<education>
{section_data}
</education>

<job_description>
{job_description}
</job_description>
</input>

<guidelines>
- Emphasize degrees, courses, and academic experiences that relate to the job.
- You are permitted to highlight coursework or adjust focus areas to better match the role.
- Relevance to the role outweighs strict adherence to the raw data.
- Follow naming conventions and match schema field names exactly.
</guidelines>

<example>
{{
  "education": [
    {{
      "degree": "MS in Computer Science",
      "institution": "Arizona State University, Tempe, USA",
      "start": "Aug 2023",
      "end": "May 2025",
      "coursework": [
        "Operational Deep Learning",
        "Social Media Mining",
        "Software Verification & Testing"
      ]
    }}
  ]
}}
</example>

{format_instructions}
"""

PROJECTS = """
<task>
Generate a structured JSON 'projects' section tailored to maximize alignment with the job description.
</task>

<input>
<projects>
{section_data}
</projects>

<job_description>
{job_description}
</job_description>
</input>

<guidelines>
- Select or adapt up to 3 projects that demonstrate capabilities most relevant to the job description.
- It is acceptable to creatively modify, combine, or extrapolate project details.
- Each project must contain: title, category, repo_url, resources (optional), start, end, and 2-3 STAR-formatted highlights.
- Use action verbs, focus on results, and match job-relevant tools/skills wherever possible.
</guidelines>

<example>
{{
  "projects": [
    {{
      "title": "Search Engine for All File Types",
      "category": "Hackathon",
      "repo_url": "https://devpost.com/software/team-soul",
      "resources": [
        {{
          "label": "Devpost Page",
          "url": "https://devpost.com/software/team-soul"
        }}
      ],
      "start": "Nov 2023",
      "end": "Nov 2023",
      "highlights": [
        "Placed 1st runner-up for AI-powered context-aware search engine using LLM-based agents.",
        "Developed TabNet classifier (98.7% accuracy) for wildfire detection with TinyML deployment.",
        "Integrated Redis/Celery backend for real-time sensor data on AWS edge devices."
      ]
    }}
  ]
}}
</example>

{format_instructions}
"""

SKILLS = """
<task>
Generate a structured JSON 'skill_section' grouped by domains, highly tailored to the job description.
</task>

<input>
<skill_section>
{section_data}
</skill_section>

<job_description>
{job_description}
</job_description>
</input>

<guidelines>
- Prioritize skills, tools, and technologies directly mentioned or highly relevant to the job description.
- Creative inference is allowed: if a tool or domain fits logically with the user's general background and the job, include it.
- Use clear domain titles and accurate tool names.
- Maximize overlap with job posting keywords naturally.
</guidelines>

<example>
{{
  "skill_section": [
    {{
      "title": "Programming Languages",
      "items": ["Python", "JavaScript", "C#"]
    }},
    {{
      "title": "Cloud & DevOps",
      "items": ["Azure", "AWS", "Docker", "Kubernetes"]
    }}
  ]
}}
</example>

{format_instructions}
"""

EXPERIENCE = """
<task>
Create a JSON 'work_experience' section that strongly matches the job description, using STAR-formatted bullet points.
</task>

<input>
<work_experience>
{section_data}
</work_experience>

<job_description>
{job_description}
</job_description>
</input>

<guidelines>
- Prioritize maximum alignment with the job description over strict fidelity to the input work_experience data.
- You are allowed to creatively extrapolate, rephrase, or invent plausible experiences based on the user's general background.
- Focus heavily on keywords, skills, responsibilities, and goals mentioned in the job description.
- Each work experience entry must have: position, employer, location, start, end, and 3-4 impact-focused contributions (use STAR format).
- Use active verbs and quantifiable results whenever possible.
- Grammar and spelling must be flawless.
</guidelines>

<example>
{{
  "work_experience": [
    {{
      "position": "Product Manager",
      "employer": "InnovateX Solutions",
      "location": "Singapore",
      "start": "Jan 2022",
      "end": "Present",
      "contributions": [
        "Led cross-functional teams to launch three SaaS products, achieving a 25% increase in ARR within the first year.",
        "Conducted market research and customer interviews to prioritize features aligned with user needs and business goals.",
        "Collaborated with engineering, marketing, and sales to ensure on-time product delivery and go-to-market success.",
        "Defined KPIs and analytics frameworks, resulting in a 30% improvement in user engagement metrics."
      ]
    }}
  ]
}}
</example>

{format_instructions}
"""