#!/usr/bin/env python3
"""Compute agreement between automated scoring and manual audit labels."""
import sys
import argparse
import pandas as pd
from pathlib import Path
from pixtrap import config


def main():
    parser = argparse.ArgumentParser(description="Compute auto vs manual audit agreement.")
    parser.add_argument("--review-file", default=None, help="Path to manual_review.csv (default: results/scored/manual_review.csv)")
    args = parser.parse_args()

    review_file = Path(args.review_file) if args.review_file else config.RESULTS_SCORED_DIR / "manual_review.csv"
    if not review_file.exists():
        print(f"Error: Review file {review_file} does not exist. Run create_manual_audit_sample.py first.")
        sys.exit(1)

    df = pd.read_csv(review_file)

    # Filter to rows where manual_label has been filled
    labeled = df[df["manual_label"].notna() & (df["manual_label"].astype(str).str.strip() != "")]
    if labeled.empty:
        print("No manual labels found in review file. Fill the 'manual_label' column first.")
        sys.exit(1)

    total = len(labeled)
    agree = sum(labeled["auto_label"] == labeled["manual_label"])
    disagree = total - agree
    agreement_rate = agree / total if total > 0 else 0.0
    disagreement_rate = 1.0 - agreement_rate

    print(f"=== Audit Agreement Summary ===")
    print(f"Total labeled rows: {total}")
    print(f"Agreement: {agree} ({agreement_rate:.1%})")
    print(f"Disagreement: {disagree} ({disagreement_rate:.1%})")
    print()

    # Confusion matrix
    print("=== Confusion Matrix (auto_label vs manual_label) ===")
    ct = pd.crosstab(labeled["auto_label"], labeled["manual_label"], margins=True)
    print(ct.to_string())
    print()

    # List disagreements
    if disagree > 0:
        print("=== Disagreement Details ===")
        dis = labeled[labeled["auto_label"] != labeled["manual_label"]]
        for _, row in dis.iterrows():
            print(f"  {row['model_key']:35s} | {row['language']:5s} | auto={row['auto_label']:20s} | manual={row['manual_label']:20s} | prompt={row['prompt_id']}")


if __name__ == "__main__":
    main()
