# import requests
# import time
# import json
# from pathlib import Path
# from tqdm import tqdm

# BASE_URL = "https://issues.apache.org/jira/rest/api/2/search"

# # Generic GET with retry + backoff
# def safe_get(url, params, max_retries=5):
#     for attempt in range(max_retries):
#         try:
#             r = requests.get(url, params=params, timeout=15)
            
#             # Handle rate limit (429) or server errors (5xx)
#             if r.status_code in [429, 500, 502, 503, 504]:
#                 wait = 2 ** attempt
#                 print(f"[WARN] Server issue ({r.status_code}). Retrying in {wait}s...")
#                 time.sleep(wait)
#                 continue
            
#             r.raise_for_status()
#             return r.json()
        
#         except requests.exceptions.RequestException as e:
#             wait = 2 ** attempt
#             print(f"[ERROR] Request failed: {e}. Retry in {wait}s...")
#             time.sleep(wait)
    
#     raise Exception("Max retries exceeded.")

# # Fetch all issues for a project, saved incrementally
# def fetch_project(project_key, save_dir="data/raw"):
#     Path(save_dir).mkdir(parents=True, exist_ok=True)

#     start = 0
#     limit = 50

#     # Resume support — check latest checkpoint
#     checkpoint_file = Path(save_dir) / f"{project_key}_checkpoint.txt"
#     if checkpoint_file.exists():
#         start = int(checkpoint_file.read_text().strip())

#     print(f"Starting {project_key} from issue index:", start)

#     while True:
#         params = {
#             "jql": f"project={project_key}",
#             "startAt": start,
#             "maxResults": limit,
#             "fields": "*all"
#         }

#         data = safe_get(BASE_URL, params)
#         issues = data.get("issues", [])

#         if not issues:
#             print(f"No more issues for {project_key}. Done ✅")
#             break

#         # Save each issue as raw JSON
#         for issue in issues:
#             issue_key = issue["key"]
#             outfile = Path(save_dir) / f"{project_key}_{issue_key}.json"
#             outfile.write_text(json.dumps(issue, indent=2))

#         start += len(issues)
#         checkpoint_file.write_text(str(start))

#         print(f"Fetched {start}/{data['total']} issues from {project_key}")

#         if start >= data['total']:
#             print(f"Completed project {project_key} ✅")
#             break


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
