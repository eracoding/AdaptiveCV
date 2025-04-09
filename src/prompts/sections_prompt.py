ACHIEVEMENTS = """
<task>
Generate a structured JSON "Achievements" resume section that aligns closely with the job description.
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
- Focus on achievements that demonstrate job-relevant strengths.
- Prioritize accuracy, clarity, and specificity.
- Use active voice and ensure error-free grammar/spelling.
</guidelines>

<example>
"achievements": [
  "Won E-yantra Robotics Competition 2018 - IITB.",
  "1st Prize in 'Prompt Engineering Hackathon 2023 for Humanities'.",
  "Awarded 'Extra Miller - 2021' at Winjit Technologies for exceptional contribution."
]
</example>

{format_instructions}
"""

CERTIFICATIONS = """
<task>
Produce a JSON "Certifications" section that highlights credentials most relevant to the job post.
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
- Include only certifications aligned with the job description.
- Ensure spelling and grammar are flawless.
</guidelines>

<example>
"certifications": [
  {
    "name": "Deep Learning Specialization",
    "by": "DeepLearning.AI, Coursera Inc.",
    "link": "https://coursera.org/verify/xyz"
  },
  {
    "name": "Backend Development",
    "by": "HKUST",
    "link": "https://coursera.org/verify/abc"
  }
]
</example>

{format_instructions}
"""

EDUCATIONS = """
<task>
Create a JSON "Education" section from the user's academic history that best supports the job description.
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
- Focus on relevance to the role.
- Prioritize specificity over generality.
- Use active voice and ensure clarity and correctness.
</guidelines>

<example>
"education": [
  {
    "degree": "MS in Computer Science",
    "university": "Arizona State University, Tempe, USA",
    "from_date": "Aug 2023",
    "to_date": "May 2025",
    "grade": "3.8/4",
    "coursework": [
      "Operational Deep Learning",
      "Social Media Mining",
      "Software Verification & Testing"
    ]
  }
]
</example>

{format_instructions}
"""

PROJECTS = """
<task>
Generate a structured JSON "Project Experience" section tailored to the job description.
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
- Include 3 job-relevant projects.
- Each project must include: name, type, link (optional), dates, and 3 STAR-formatted bullet points.
- Use active voice and quantify impact when possible.
</guidelines>

<example>
"projects": [
  {
    "name": "Search Engine for All File Types",
    "type": "Hackathon",
    "link": "https://devpost.com/software/team-soul",
    "from_date": "Nov 2023",
    "to_date": "Nov 2023",
    "description": [
      "Placed 1st runner-up for AI-powered context-aware search engine using LLM-based agents.",
      "Developed TabNet classifier (98.7% accuracy) for wildfire detection with TinyML deployment.",
      "Integrated Redis/Celery backend for real-time sensor data on AWS edge devices."
    ]
  }
]
</example>

{format_instructions}
"""

SKILLS = """
<task>
Generate a structured JSON "Skills" section based on the user's technical and soft skills, aligned with the job description.
</task>

<input>
<skills>
{section_data}
</skills>

<job_description>
{job_description}
</job_description>
</input>

<guidelines>
- Prioritize job-specific skills.
- Group skills by category (e.g., Programming Languages, DevOps).
- Ensure consistent formatting and error-free grammar.
</guidelines>

<example>
"skill_section": [
  {
    "name": "Programming Languages",
    "skills": ["Python", "JavaScript", "C#"]
  },
  {
    "name": "Cloud & DevOps",
    "skills": ["Azure", "AWS", "Docker", "Kubernetes"]
  }
]
</example>

{format_instructions}
"""

EXPERIENCE = """
<task>
Create a job-targeted JSON "Work Experience" section using STAR-formatted bullet points.
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
- Include 3 relevant job roles.
- Each job should have: role, company, location, dates, and 3 bullet points.
- Use measurable impact and STAR logic: Situation → Task → Action → Result.
- Follow “Did X by doing Y, achieved Z” structure.
- Prioritize truthfulness, clarity, and strong action verbs.
</guidelines>

<example>
"work_experience": [
  {
    "role": "Software Engineer",
    "company": "Winjit Technologies",
    "location": "Pune, India",
    "from_date": "Jan 2020",
    "to_date": "Jun 2022",
    "description": [
      "Built and scaled 10+ REST APIs and 30+ UI components; improved system responsiveness by 85%.",
      "Led dev of dynamic form generator; reduced front-end development time by 8x.",
      "Optimized backend workflows and databases for high-traffic systems across 3 departments."
    ]
  }
]
</example>

{format_instructions}
"""
