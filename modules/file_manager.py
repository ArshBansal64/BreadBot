import csv
import os
from collections import Counter
from typing import Optional

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
KEYWORDS_DIR = os.path.join(BASE_DIR, "keywords")


def ensure_project_dirs() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(KEYWORDS_DIR, exist_ok=True)


def get_run_dir(run_stamp: str) -> str:
    run_dir = os.path.join(KEYWORDS_DIR, run_stamp)
    os.makedirs(run_dir, exist_ok=True)
    return run_dir


def save_run_jobs_csv(job_df: pd.DataFrame, run_stamp: str) -> str:
    run_dir = get_run_dir(run_stamp)

    out_path = os.path.join(run_dir, f"jobs_{run_stamp}.csv")
    job_df.to_csv(out_path, index=False)

    print("Saved jobs csv:", os.path.abspath(out_path))
    return out_path


def save_run_keywords_snapshot(counts: Counter, run_stamp: str) -> str:
    run_dir = get_run_dir(run_stamp)

    out_path = os.path.join(run_dir, f"keywords_{run_stamp}.csv")
    _write_keywords_csv(out_path, counts)

    print("Saved keywords snapshot:", os.path.abspath(out_path))
    return out_path


def update_cumulative_keywords(
    run_counts: Counter,
    cumulative_path: Optional[str] = None
) -> str:
    os.makedirs(KEYWORDS_DIR, exist_ok=True)

    if cumulative_path is None:
        cumulative_path = os.path.join(KEYWORDS_DIR, "keywords.csv")

    existing = Counter()

    if os.path.exists(cumulative_path):
        with open(cumulative_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            first_row = True
            for row in reader:
                if not row or len(row) < 2:
                    continue

                if first_row and row[0].strip().lower() == "keyword":
                    first_row = False
                    continue
                first_row = False

                keyword = row[0].strip()
                freq_str = row[1].strip()

                if not keyword:
                    continue

                try:
                    existing[keyword] += int(freq_str)
                except Exception:
                    continue

    for keyword, freq in run_counts.items():
        existing[keyword] += int(freq)

    _write_keywords_csv(cumulative_path, existing)

    print("Updated master keywords:", os.path.abspath(cumulative_path))
    return cumulative_path


def _write_keywords_csv(path: str, counts: Counter) -> None:
    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["keyword", "frequency"])
        for keyword, freq in items:
            writer.writerow([keyword, int(freq)])
