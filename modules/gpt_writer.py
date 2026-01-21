import json
import re
from typing import List


def _normalize_keyword(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s


def extract_keywords(description: str, api_key: str, model: str = "gpt-4o-mini") -> List[str]:
    description = description or ""
    if not description.strip():
        return []

    system = (
        "You extract skill keywords from job descriptions.\n"
        "Return JSON only.\n"
        "No commentary."
    )

    user = (
        "From the job description below, extract a list of concise skill keywords.\n"
        "Rules:\n"
        "  - Use short phrases (1 to 3 words) when needed.\n"
        "  - Prefer technical skills, tools, frameworks, platforms, and core concepts.\n"
        "  - Do not include soft skills, benefits, locations, or generic words.\n"
        "  - Keep original casing when it is meaningful (AWS, C++, PyTorch).\n"
        "Output JSON with this shape:\n"
        "{\n"
        '  "keywords": ["React", "AWS", "Python"]\n'
        "}\n\n"
        "JOB DESCRIPTION:\n"
        f"{description}"
    )

    try:
        from openai import OpenAI  # new SDK
        client = OpenAI(api_key=api_key)

        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.0,
        )
        text = resp.choices[0].message.content

    except Exception:
        import openai  # old SDK

        openai.api_key = api_key
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.0,
        )
        text = resp["choices"][0]["message"]["content"]

    data = None
    try:
        data = json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if m:
            try:
                data = json.loads(m.group(0))
            except Exception:
                data = None

    if not isinstance(data, dict) or "keywords" not in data:
        return []

    kws = data.get("keywords", [])
    if not isinstance(kws, list):
        return []

    cleaned = []
    seen = set()
    for kw in kws:
        if not isinstance(kw, str):
            continue
        kw = _normalize_keyword(kw)
        if not kw:
            continue
        if kw.lower() in seen:
            continue
        seen.add(kw.lower())
        cleaned.append(kw)

    return cleaned
