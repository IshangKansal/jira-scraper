import os
import json
import time
import requests
from tqdm import tqdm

BASE_URL = "https://issues.apache.org/jira/rest/api/2/search"

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

def fetch_project_issues(project):
    start = 0
    max_results = 50

    while True:
        params = {
            "jql": f"project={project}",
            "startAt": start,
            "maxResults": max_results
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"⚠ Error {response.status_code}, retrying...")
            time.sleep(5)
            continue

        data = response.json()
        issues = data.get("issues", [])

        if not issues:
            break

        for issue in tqdm(issues, desc=f"{project}"):
            issue_id = issue["key"]
            out_file = f"{RAW_DIR}/{issue_id}.json"

            if not os.path.exists(out_file):
                with open(out_file, "w", encoding="utf-8") as f:
                    json.dump(issue, f, ensure_ascii=False)

        start += max_results

    print(f"✅ Finished {project}")
