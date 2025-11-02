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

            if os.path.exists(out_file):
                continue

            # Fetch full issue details WITH comments
            issue_url = f"https://issues.apache.org/jira/rest/api/2/issue/{issue_id}"
            issue_response = requests.get(issue_url, params={"expand": "comments"})

            if issue_response.status_code != 200:
                print(f"⚠ Could not fetch details for {issue_id}, skipping...")
                continue

            full_issue = issue_response.json()

            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(full_issue, f, ensure_ascii=False)


        # for issue in tqdm(issues, desc=f"{project}"):
        #     issue_id = issue["key"]
        #     out_file = f"{RAW_DIR}/{issue_id}.json"

        #     # Skip if already downloaded (resumable)
        #     if os.path.exists(out_file):
        #         continue

        #     # Fetch full issue details **with comments**
        #     issue_url = f"https://issues.apache.org/jira/rest/api/2/issue/{issue_id}?expand=renderedFields,comment"
        #     full_resp = requests.get(issue_url)

        #     # Retry logic for rate limits / 5xx
        #     retries = 3
        #     while full_resp.status_code in (429, 502, 503, 504) and retries > 0:
        #         time.sleep(3)
        #         full_resp = requests.get(issue_url)
        #         retries -= 1

        #     if full_resp.status_code != 200:
        #         print(f"⚠ Failed to fetch {issue_id}, status {full_resp.status_code}")
        #         continue

        #     full_issue_data = full_resp.json()

        #     with open(out_file, "w", encoding="utf-8") as f:
        #         json.dump(full_issue_data, f, ensure_ascii=False, indent=2)


        # for issue in tqdm(issues, desc=f"{project}"):
        #     issue_id = issue["key"]
        #     out_file = f"{RAW_DIR}/{issue_id}.json"

        #     if not os.path.exists(out_file):
        #         with open(out_file, "w", encoding="utf-8") as f:
        #             json.dump(issue, f, ensure_ascii=False)

        start += max_results

    print(f"✅ Finished {project}")
