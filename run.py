from scraper.fetcher import fetch_project_issues

projects = ["JENA", "NUTCH"]  # change to ["SPARK","KAFKA","HADOOP"] later

if __name__ == "__main__":
    for project in projects:
        print(f"\n=== Fetching {project} ===")
        fetch_project_issues(project)
