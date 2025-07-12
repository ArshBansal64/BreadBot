import requests
from bs4 import BeautifulSoup

def extract_job_description(link):
    try:
        response = requests.get(link, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)[:4000]  # truncate for GPT
    except Exception as e:
        return "Job description could not be retrieved."