#!/usr/bin/env python3
import sys
import argparse
import json
import pandas as pd
from pathlib import Path
from pixtrap import config
from pixtrap.scoring import score_output

def main():
    parser = argparse.ArgumentParser(description="Score PixTrap evaluation outputs.")
    parser.add_argument("--run-id", required=True, help="Run ID of the evaluation to score.")
    args = parser.parse_args()

    raw_file = config.RESULTS_RAW_DIR / f"results_{args.run_id}.jsonl"
    if not raw_file.exists():
        print(f"Error: Raw results file {raw_file} does not exist.")
        sys.exit(1)

    print(f"Scoring results from {raw_file}...")
    records = []
    with open(raw_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                # Score the record
                label = score_output(record)
                record["auto_label"] = label
                records.append(record)
            except Exception as e:
                print(f"Error parsing/scoring line: {e}")

    if not records:
        print("No records found to score.")
        sys.exit(1)

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(records)

    # Drop raw_response from the scored CSV — it bloats the file with full API
    # payloads (including reasoning traces). The raw JSONL remains the full-fidelity archive.
    if "raw_response" in df.columns:
        df = df.drop(columns=["raw_response"])
    
    # Ensure scored directory exists
    config.RESULTS_SCORED_DIR.mkdir(parents=True, exist_ok=True)
    scored_csv = config.RESULTS_SCORED_DIR / f"results_{args.run_id}_scored.csv"
    
    df.to_csv(scored_csv, index=False)
    print(f"Scored {len(df)} records. Saved to {scored_csv}")

    # Print summary counts of labels
    print("\nScore Label Summary:")
    print(df["auto_label"].value_counts().to_string())

if __name__ == "__main__":
    main()
