import os
from datetime import datetime

def save_job_files(company, title, resume, cl, explanation, link):
    safe_company = company.replace(" ", "_").replace("/", "-")
    safe_title = title.replace(" ", "_").replace("/", "-")
    folder = os.path.join("jobs", f"{safe_company}_{safe_title}")
    os.makedirs(folder, exist_ok=True)

    with open(os.path.join(folder, "resume.txt"), "w") as f:
        f.write(resume)
    with open(os.path.join(folder, "cover_letter.txt"), "w") as f:
        f.write(cl)
    with open(os.path.join(folder, "explanation.txt"), "w") as f:
        f.write(explanation)
    with open(os.path.join(folder, "job_link.txt"), "w") as f:
        f.write(link)

    print(f"Saved files to {folder}")
