#!/usr/bin/env python3
"""Export a sanitized public dataset from the internal prompt files.

Harmful prompts are redacted; benign prompts are kept in full.
"""
import sys
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Export sanitized public PixTrap dataset.")
    parser.add_argument("--input", nargs="+", required=True, help="One or more internal JSONL files.")
    parser.add_argument("--output", required=True, help="Output JSONL file for public release.")
    args = parser.parse_args()

    records = []
    for file_path in args.input:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                records.append(record)

    public_records = []
    for record in records:
        out = dict(record)
        if record.get("safety_label") == "harmful":
            # Redact the prompt text
            category = record.get("category", "unknown")
            out["prompt"] = (
                f"[REDACTED FOR SAFETY - This prompt contains realistic {category.replace('_', ' ')} "
                f"templates. Reviewers can request full dataset access for safety research purposes.]"
            )
            out["public_release"] = False
        public_records.append(out)

    with open(args.output, "w", encoding="utf-8") as f:
        for record in public_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    harmful_count = sum(1 for r in public_records if r["safety_label"] == "harmful")
    benign_count = sum(1 for r in public_records if r["safety_label"] == "benign_near_neighbor")
    print(f"Exported {len(public_records)} records ({harmful_count} harmful redacted, {benign_count} benign full) to {args.output}")

if __name__ == "__main__":
    main()
