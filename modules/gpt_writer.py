import openai
import os

TEMPLATE_RESUME_PATH = os.path.join("templates", "resume_template.txt")
TEMPLATE_CL_PATH = os.path.join("templates", "cover_letter_template.txt")

def generate_documents(job_description, link, api_key):
    openai.api_key = api_key

    with open(TEMPLATE_RESUME_PATH) as f:
        base_resume = f.read()
    with open(TEMPLATE_CL_PATH) as f:
        base_cl = f.read()

    prompt = f"""
You are an AI assistant helping tailor job applications.

Job Description:
{job_description}

Base Resume:
{base_resume}

Base Cover Letter:
{base_cl}

Return:
1. Tailored resume
2. Tailored cover letter
3. Explanation of changes
Also extract job title and company name if available.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    # crude parsing assuming structured GPT response
    sections = content.split("###")
    resume = sections[1].strip()
    cover_letter = sections[2].strip()
    explanation = sections[3].strip()
    job_title = sections[4].strip() if len(sections) > 4 else "Unknown_Title"
    company = sections[5].strip() if len(sections) > 5 else "Unknown_Company"

    return resume, cover_letter, explanation, job_title, company