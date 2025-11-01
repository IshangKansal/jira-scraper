# import json
# from glob import glob
# from pathlib import Path

# def classify(text):
#     text = text.lower()
#     if any(w in text for w in ["error", "fail", "bug", "broken", "incorrect", "exception"]):
#         return "bug"
#     if any(w in text for w in ["feature", "add", "enhance", "support", "implement"]):
#         return "feature-request"
#     if any(w in text for w in ["document", "doc", "javadoc", "guide", "readme"]):
#         return "documentation"
#     return "other"


# def extract_text(field):
#     if not field:
#         return ""
#     if isinstance(field, str):
#         return field.replace("\r", "").replace("\n", " ").strip()
#     return ""

# def parse_issue(raw_issue):
#     key = raw_issue["key"]
#     fields = raw_issue.get("fields", {})

#     title = extract_text(fields.get("summary"))
#     description = extract_text(fields.get("description"))

#     comments_block = fields.get("comment") or {}

#     comments = []
#     for c in comments_block.get("comments", []):
#         comments.append(extract_text(c.get("body")))

#     reporter = fields.get("reporter")
#     assignee = fields.get("assignee")

#     record = {
#         "issue_id": key,
#         "project": key.split("-")[0],
#         "title": title,
#         "status": fields.get("status", {}).get("name"),
#         "priority": fields.get("priority", {}).get("name"),
#         "reporter": reporter.get("displayName") if reporter else None,
#         "assignee": assignee.get("displayName") if assignee else None,
#         "created": fields.get("created"),
#         "updated": fields.get("updated"),
#         "description": description,
#         "comments": comments,
#     }

#     summary = title
#     classification = classify(title + " " + description)
#     qa_pairs = [
#         {
#             "question": "What is the issue about?",
#             "answer": summary
#         },
#         {
#             "question": "What context is given in the description?",
#             "answer": description if description else "No description provided."
#         }
#     ]

#     record["tasks"] = {
#         "summary": summary,
#         "classification": classification,
#         "qa_pairs": qa_pairs
#     }


#     return record


def parse_issue(issue):
    fields = issue.get("fields", {}) or {}

    return {
        "issue_id": issue.get("key"),
        "project": fields.get("project", {}).get("key"),
        "title": fields.get("summary"),
        "status": fields.get("status", {}).get("name"),
        "priority": (fields.get("priority") or {}).get("name"),
        "reporter": (fields.get("reporter") or {}).get("displayName"),
        "assignee": (fields.get("assignee") or {}).get("displayName"),
        "created": fields.get("created"),
        "updated": fields.get("updated"),
        "description": fields.get("description"),
        "comments": [
            c.get("body")
            for c in (fields.get("comment", {}).get("comments") or [])
            if c.get("body")
        ],
        "tasks": {
            "summary": fields.get("summary"),
            "classification": infer_classification(fields),
            "qa_pairs": generate_qa_pairs(fields)
        }
    }

def infer_classification(fields):
    summary = (fields.get("summary") or "").lower()
    if any(w in summary for w in ["bug", "fix", "error", "fail"]):
        return "bug"
    return "task"

def generate_qa_pairs(fields):
    summary = fields.get("summary") or ""
    desc = fields.get("description") or ""
    if not summary or not desc:
        return []
    return [
        {"question": "What is the issue about?", "answer": summary},
        {"question": "What is the main context?", "answer": desc[:200]}
    ]
