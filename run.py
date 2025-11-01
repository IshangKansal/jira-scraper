# from scraper.fetcher import fetch_project

# projects = ["NUTCH", "TIKA", "JENA"]

# for p in projects:
#     fetch_project(p)

from scraper.fetcher import fetch_project_issues

projects = ["NUTCH", "TIKA", "JENA"]  # change to ["SPARK","KAFKA","HADOOP"] later

if __name__ == "__main__":
    for project in projects:
        print(f"\n=== Fetching {project} ===")
        fetch_project_issues(project)
