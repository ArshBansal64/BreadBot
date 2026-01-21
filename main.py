import logging
import os
from collections import Counter

import pandas as pd
from dotenv import load_dotenv

from modules.gpt_writer import extract_keywords
from modules.file_manager import (
    ensure_project_dirs,
    save_run_jobs_csv,
    save_run_keywords_snapshot,
    update_cumulative_keywords,
)



logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def read_jobs_table(path: str) -> pd.DataFrame:
    if path.lower().endswith(".xlsx") or path.lower().endswith(".xls"):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)

    df.columns = [str(c).strip() for c in df.columns]
    needed = ["Position", "Company", "Location", "Description"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["Position"] = df["Position"].fillna("").astype(str)
    df["Company"] = df["Company"].fillna("").astype(str)
    df["Location"] = df["Location"].fillna("").astype(str)
    df["Description"] = df["Description"].fillna("").astype(str)

    df = df[df["Description"].str.strip().ne("")].reset_index(drop=True)
    return df


def main() -> int:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Missing OPENAI_API_KEY in environment.")
        return 1

    ensure_project_dirs()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(BASE_DIR, "data", "jobs.csv")

    try:
        job_df = read_jobs_table(input_path)
    except Exception as e:
        print(e)
        logging.error("Failed reading input jobs file", exc_info=True)
        return 1

    run_stamp = pd.Timestamp.utcnow().strftime("%Y%m%d_%H%M%S")

    print("Jobs loaded:", len(job_df))

    run_counts = Counter()

    for _, row in job_df.iterrows():
        company = row["Company"].strip() or "(Unknown Company)"
        position = row["Position"].strip() or "(Unknown Position)"
        description = row["Description"]

        try:
            keywords = extract_keywords(description=description, api_key=api_key)
            for kw in keywords:
                run_counts[kw] += 1

            print("Processed:", company, "-", position)

        except Exception as e:
            print("Error on:", company, "-", position)
            print(e)
            logging.error(f"Error processing job: {company} - {position}\n{str(e)}", exc_info=True)

    if not run_counts:
        print("No keywords were generated.")
        save_run_jobs_csv(job_df, run_stamp)
        return 0

    save_run_jobs_csv(job_df, run_stamp)
    save_run_keywords_snapshot(run_counts, run_stamp)
    update_cumulative_keywords(run_counts)

    print("Run keywords saved as:", f"keywords/keywords_{run_stamp}.csv")
    print("Cumulative keywords updated:", "keywords/keywords.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
