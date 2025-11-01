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
