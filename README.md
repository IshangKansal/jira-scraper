# 🐍 Apache Jira Scraping & LLM Training Dataset Pipeline

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![Data Pipeline](https://img.shields.io/badge/Workflow-Scrape→Clean→Train-green)]()
[![License](https://img.shields.io/badge/License-Apache_2.0-yellow)]()
[![Status](https://img.shields.io/badge/Build-Stable-brightgreen)]()

This project implements a **fault-tolerant, resumable, and scalable** data scraping pipeline for extracting issue data from **Apache’s public Jira instance**, and converting it into a **structured JSONL dataset suitable for LLM training**.

---

## ✅ Features

| Feature | Description |
|--------|-------------|
| **Resumable Scraping** | Automatically skips already-downloaded issues |
| **Pagination & Retry Handling** | Safe retries for network failures + rate limits |
| **Clean JSONL Output** | Normalized metadata + comments + timestamps |
| **Task Derivation** | Auto-generates summary, classification, and Q/A pairs |
| **Sharded Output** | JSONL shards for efficient streaming into LLM training |

---

## 🏗️ Pipeline Architecture

         ┌──────────────────┐
         │  Apache Jira API │
         └─────────┬────────┘
                   │
         (Pagination, Retries)
                   │
        ┌──────────▼──────────┐
        │   Scraper (fetcher) │
        └──────────┬──────────┘
                   │
           Raw JSON Writes
                   │
       ┌───────────▼────────────┐
       │     data/raw/*.json    │
       └───────────┬────────────┘
                   │
          Cleaning + Structuring
                   │
       ┌───────────▼────────────┐
       │ parser.py (transform)  │
       └───────────┬────────────┘
                   │
           JSONL Sharded Output
                   │
     ┌─────────────▼────────────────┐
     │ data/processed/shards/*.jsonl│
     └──────────────────────────────┘


---

## 📂 Directory Layout

jira-scraper/
│
├── run.py # Scrape selected Jira projects
├── convert_raw_to_clean.py # Convert raw → structured JSONL
├── requirements.txt
├── Makefile
├── .gitignore
│
├── scraper/
│ ├── fetcher.py # Handles API calls, retries, pagination
│ └── parser.py # Cleans data + generates tasks
│
└── data/
├── raw/ # Raw downloaded issues
└── processed/
    └── shards/ # Clean JSONL dataset ready for training


---

## 🛠️ Setup Instructions

### 1) Clone & Install Dependencies

```bash
git clone <your-repo-url>
cd jira-scraper
pip install -r requirements.txt
```

### 2) Create Required Folders

```bash
mkdir -p data/raw data/processed/shards
```

---

## 🚀 Step 1 — Scrape Apache Jira Issues

Modify the `projects` list inside **run.py** to select which Apache Jira projects to scrape:

```python
projects = ["NUTCH", "TIKA", "JENA"]
```

Then run the scraper:

```bash
python run.py
```

This will download raw issue JSON files to:

```bash
data/raw/
```

Each file corresponds to a single Jira issue (e.g., JENA-1.json).

## 🧹 Step 2 — Convert to Clean JSONL Dataset

Once scraping is complete, convert the raw data:

```bash
python convert_raw_to_clean.py
```

Cleaned and standardized training-ready output will be stored in:

```bash
data/processed/shards/
```

Each shard_*.jsonl file contains one JSON object per line, ready for LLM ingestion.

## 🧾 Example Output Record

```json
{
  "issue_id": "JENA-1",
  "project": "JENA",
  "title": "No web site at the Apache Incubator yet",
  "status": "Closed",
  "priority": "Major",
  "reporter": "umesh awasthi",
  "assignee": "Ian Dickinson",
  "created": "2010-12-08T16:40:04.000+0000",
  "updated": "2015-02-01T19:11:31.000+0000",
  "description": "Tried to access the webpage for Jena but received a 404 error.",
  "comments": [
    "A redirect is not a good idea...",
    "There is a website at http://incubator.apache.org/jena now."
  ],
  "tasks": {
    "summary": "Missing Apache Jena incubator website",
    "classification": "bug",
    "qa_pairs": [
      {
        "question": "What is the issue about?",
        "answer": "The Apache Jena incubator website was missing and returned a 404."
      },
      {
        "question": "What context is provided?",
        "answer": "The user attempted to access the site and encountered a 404 error."
      }
    ]
  }
}
```

---

## 🌱 Future Improvements

We plan to enhance the pipeline in the following ways:

| Improvement | Benefit |
|------------|---------|
| **Parallel / Distributed Scraping** | Speed up data collection across large Jira project histories |
| **Issue Deduplication & Cross-Project Linking** | Avoid redundant samples and improve dataset quality |
| **ML-Based Labeling Enhancements** | Move beyond rule-based classification to learned topic tagging |
| **Automatic Multi-Step Q/A Generation** | Create richer LLM training samples for reasoning tasks |
| **Dataset Quality Metrics Dashboard** | Track data volume, task diversity, and distribution balance |
| **Vector Storage / Semantic Search Index** | Allow fast retrieval of similar issues for fine-tuning loops |

---


