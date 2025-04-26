# AdaptiveCV: AI-powered Resume Generation and Optimization

## Overview
AdaptiveCV is an advanced AI-driven platform designed to automatically generate, optimize, and personalize resumes tailored to specific job descriptions.Leveraging Large Language Models (LLMs), AdaptiveCV helps job seekers create high-quality, ATS-friendly, and recruiter-optimized resumes — significantly increasing interview opportunities with minimal manual effort.

## Problem Statement
Creating job-specific resumes increases interview chances but remains an impractical task due to its time-consuming nature. Traditional methods of resume tailoring are either manual and resource-intensive or rely on simplistic keyword matching and static templates, failing to dynamically adjust to unique job requirements.

AdaptiveCV addresses this challenge by providing a fully automated, intelligent resume generation and optimization solution that dynamically tailors content to specific job descriptions.

## Features
1. Resume Generation: Create a brand-new, structured resume aligned with a specific job description based on user input or uploaded data.
2. Resume Optimization: Upload an existing resume and intelligently improve it to match recruiter expectations and ATS standards.
3. Resume Metrics: Evaluate resume effectiveness based on personalization, job alignment, and original match scores.
4. Interactive Web App: Easy-to-use Streamlit-based UI to generate, download, edit in Overleaf, and analyze resumes.

## Project Structure
Possible project structure:
```
AdaptiveCV
├── app/                      # Frontend application on Next.js
├── media/                    # All media content
├── datasets/                 # Available resumes and job postings to evaluate the pipeline performance
│   ├── resumes/
│   └── job_postings/
├── output/                   # Generated resumes and cover letters
├── src/                      # AdaptiveCV src code
│   ├── adaptivecv.py         # AdaptiveCV pipeline definition
│   ├── utils/
│   │   ├── job_ops.py        # File operations and preprocessing functions
│   │   ├── latex_ops.py      # Latex generation support functions
│   │   ├── metrics.py        # Calculating metrics functions
│   │   └── text_ops.py       # Text processing functions
│   └── templates/            # Defined templates for Latex generation
│       ├── resume.cls        # Main latex document
│       └── resume.tex.jinja  # Latex Template
├── uploads/                  # User uploaded documents (pdf, json)
├── README.md                 # Repo description
├── poetry.lock               # Poetry lock required for environment configuration
├── pyproject.toml            # Poetry environment configuration
├── main.py                   # Main application CLI entrypoint
├── streamlit_app.py          # Web Streamlit App to deploy
├── .env_example              # Environment variables
└── requirements.txt          # Installation files

```

## Methodology

![](https://github.com/eracoding/AdaptiveCV/blob/main/media/pipeline.png)

### Workflow:
1. **User Input**: Upload resume or enter professional details.
2. **Job Parsing**: Extract key skills and requirements from job descriptions.
3. **Data Aggregation**: Combine user data and job info.
4. **LLM Processing**: Generate or optimize resumes aligned to the job.
5. **Web Interface**: Download, edit, and evaluate resume content.

---

### Core System Pipeline
- **Job Description Parsing**: Extracts essential qualifications, skills, and keywords.
- **User Resume Processing**: Analyzes uploaded resumes or inputted details.
- **Resume Generation and Optimization**: Produces structured, targeted resumes to optimize ATS compatibility and recruiter appeal.

### Datasets and Preprocessing
- **Datasets**: Utilizes publicly available datasets of resumes and job postings.
- **Preprocessing Steps**:
  - Text Cleaning
  - Tokenization
  - Entity Extraction (skills, qualifications, etc.)

## Evaluation Metrics
The effectiveness of AdaptiveCV will be measured through:
- **Job Alignment Score**: Evaluates the match between the resume and job requirements (keyword coverage and semantic similarity).
- **Content Preservation Score**: Ensures factual accuracy, avoiding misrepresentation or hallucination by the LLM.

## Usage

### Quick Start Example:
```bash
poetry install
poetry run python main.py --job-url "link/to/job_posting" --user-data "src/demo/user_profile.json/pdf"
```

Or use the **Streamlit App**:
```bash
poetry run streamlit run streamlit_app.py
```

---

### User Workflow
1. Enter personal details manually or upload an existing resume file.
2. Provide or select a target job description.
3. Generate a resume tailored to the job.
4. Review resume effectiveness metrics.
5. Download the final resume or edit further in Overleaf.

---

## Benefits
- **Save time** and automate resume tailoring.
- **Optimize ATS compatibility** for better visibility.
- **Increase recruiter interest** through dynamic content alignment.
- **Interactive editing** and visualization for users.

---

## Limitations and Future Work
- Dependent on the quality of user input and job description parsing accuracy.
- Future improvements could include:
  - Real-world dataset fine-tuning.
  - Multilingual support.
  - Direct integration with job boards and recruitment platforms.
  - Continuous learning from user feedback loops.

---

## Conclusion
AdaptiveCV offers a **practical, scalable solution** for job seekers to maximize their chances of landing interviews.  
By combining intelligent job parsing, user data analysis, and advanced LLM generation, AdaptiveCV dynamically creates recruiter-friendly and ATS-optimized resumes customized to each opportunity.

---

## Demo

![](https://github.com/eracoding/AdaptiveCV/blob/main/media/demo.gif)

🎮 **Demo Video:** [Watch here](https://youtu.be/uzpDKVsP7iI)

---
