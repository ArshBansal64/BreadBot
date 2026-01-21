# Breadbot - Job Keyword Analysis

This project analyzes keywords found in software engineering and data science job descriptions and visualizes trends in employer demand.

## Overview
Breadbot is a lightweight analysis pipeline that processes job description text, extracts technical keywords using a language model, aggregates frequencies, and produces visual summaries. The goal is to understand which skills and technologies appear most frequently across a broad set of roles.

## Data
The data folder contains a sample jobs.csv file used to demonstrate the pipeline. This file is not the original dataset used for analysis. The original analysis was performed on a larger private dataset (500+ jobs) collected over a fixed time window. The sample file exists only to make the project runnable and reproducible.

## Pipeline Summary
1. Job descriptions are loaded from a CSV file.
2. Each description is passed to a keyword extraction step powered by the OpenAI API.
3. Extracted keywords are counted and aggregated.
4. Results are written to:
   - keywords/keywords.csv (cumulative keyword counts)
   - keywords/<timestamp>/ (per-run snapshots of jobs and keywords)
5. An R script generates visualizations from the keyword data.

## Keyword Storage
The keywords folder contains:
- keywords.csv: a cumulative master file updated across runs
- timestamped subfolders: each run stores its own jobs and keyword snapshot to preserve history and reproducibility

## Visualizations
The scripts/keywordVisualization.R script generates:
- A bar chart of the top keywords
- A word cloud showing relative keyword frequency

Example outputs are included in the visualizations folder. The R script is meant to be run manually after a sufficient sum of data has been collected and aggregated.
<img width="2048" height="1536" alt="Bar Chart" src="https://github.com/user-attachments/assets/8327fef5-9cee-497e-9c7e-d6e88ff9ef0a" />


## Reproducibility
Each run is timestamped so results can be traced back to a specific input dataset. This design avoids overwriting results and allows comparisons across runs.

## Setup
1. Create a virtual environment
2. Install dependencies
3. Copy .env.example to .env and add your OpenAI API key
4. Upload/update data/jobs.csv with custom data
5. Run main.py
6. Run the R script to generate visualizations
