#!/usr/bin/env python3
import sys
import argparse
from pixtrap.dataset import load_dataset

def main():
    parser = argparse.ArgumentParser(description="Validate a PixTrap JSONL dataset.")
    parser.add_argument("dataset_files", nargs="+", help="Path to one or more JSONL files.")
    args = parser.parse_args()

    success = True
    for file_path in args.dataset_files:
        try:
            records = load_dataset(file_path)
            harmful_count = sum(1 for r in records if r.safety_label == "harmful")
            benign_count = sum(1 for r in records if r.safety_label == "benign_near_neighbor")
            ptbr_count = sum(1 for r in records if r.language == "pt-BR")
            en_count = sum(1 for r in records if r.language == "en")

            print(f"File: {file_path}")
            print(f"  Total records: {len(records)}")
            print(f"  Harmful: {harmful_count}")
            print(f"  Benign Near-Neighbors: {benign_count}")
            print(f"  pt-BR: {ptbr_count}")
            print(f"  en: {en_count}")
            print("  Status: VALID")
        except Exception as e:
            print(f"File: {file_path}")
            print(f"  Status: INVALID")
            print(f"  Error: {e}")
            success = False

    if not success:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
