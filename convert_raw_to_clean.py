# import json
# from pathlib import Path
# from scraper.parser import parse_issue

# RAW_DIR = Path("data/raw")
# SHARD_DIR = Path("data/processed/shards")
# SHARD_DIR.mkdir(parents=True, exist_ok=True)

# SHARD_SIZE = 5000  # one shard per 5000 issues

# def convert():
#     shard_index = 0
#     count = 0
#     outfile = None

#     for raw_file in RAW_DIR.glob("*.json"):
#         if count % SHARD_SIZE == 0:
#             if outfile:
#                 outfile.close()
#             shard_index += 1
#             outfile = SHARD_DIR / f"issues_{shard_index:05d}.jsonl"
#             outfile = outfile.open("w")

#         data = json.loads(raw_file.read_text())
#         cleaned = parse_issue(data)
#         outfile.write(json.dumps(cleaned) + "\n")
#         count += 1

#     if outfile:
#         outfile.close()

# if __name__ == "__main__":
#     convert()

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

