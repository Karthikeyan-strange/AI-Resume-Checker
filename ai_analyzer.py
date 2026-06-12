import os, json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile" # free & fast | alternatives below


def _ask(prompt: str) -> str:
    """Send a prompt to Groq and return raw text."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def parse_resume(resume_text: str) -> dict:
    prompt = f"""
Extract the following fields from this resume.
Return ONLY a valid JSON object — no markdown, no explanation, no backticks.

Fields:
- name (string)
- email (string)
- phone (string)
- skills (list of strings)
- education (list of objects: degree, institution, year)
- experience (list of objects: title, company, duration, description)

Resume:
{resume_text}

JSON only:
"""
    raw = _ask(prompt).replace("```json", "").replace("```", "")
    return json.loads(raw)


def match_resume_to_job(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are a professional HR recruiter. Analyze the resume against the job description.
Return ONLY a valid JSON object — no markdown, no explanation, no backticks.

Fields:
- match_score (integer 0-100)
- matched_skills (list of strings)
- missing_skills (list of strings)
- strengths (list of 3-5 strings)
- weaknesses (list of 2-4 strings)
- recommendation (one of: "Strong Fit", "Moderate Fit", "Weak Fit")
- summary (2-3 sentence string)

Resume:
{resume_text}

Job Description:
{job_description}

JSON only:
"""
    raw = _ask(prompt).replace("```json", "").replace("```", "")
    return json.loads(raw)


