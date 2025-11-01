import json
import os
from scraper.parser import parse_issue

RAW_DIR = "data/raw"
OUT_DIR = "data/processed/shards"

def convert():
    os.makedirs(OUT_DIR, exist_ok=True)

    shard = 0
    count = 0
    shard_file = open(f"{OUT_DIR}/shard_{shard}.jsonl", "w", encoding="utf-8")

    for filename in os.listdir(RAW_DIR):
        path = os.path.join(RAW_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        cleaned = parse_issue(data)
        if cleaned:
            shard_file.write(json.dumps(cleaned, ensure_ascii=False) + "\n")
            count += 1

            # new shard every 5000 records
            if count % 5000 == 0:
                shard += 1
                shard_file.close()
                shard_file = open(f"{OUT_DIR}/shard_{shard}.jsonl", "w", encoding="utf-8")

    shard_file.close()
    print(f"✅ Conversion complete. Total cleaned records: {count}")

if __name__ == "__main__":
    convert()

