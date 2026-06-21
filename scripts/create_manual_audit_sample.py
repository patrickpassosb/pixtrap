#!/usr/bin/env python3
import sys
import argparse
import pandas as pd
from pathlib import Path
from pixtrap import config

def main():
    parser = argparse.ArgumentParser(description="Create a stratified manual audit sample.")
    parser.add_argument("--run-id", required=True, help="Run ID of the evaluation to sample.")
    parser.add_argument("--sample-size", type=int, default=30, help="Target total sample size (default: 30).")
    args = parser.parse_args()

    scored_csv = config.RESULTS_SCORED_DIR / f"results_{args.run_id}_scored.csv"
    if not scored_csv.exists():
        print(f"Error: Scored CSV file {scored_csv} does not exist. Run scoring first.")
        sys.exit(1)

    df = pd.read_csv(scored_csv)
    
    # Stratified sampling
    # We group by model_key, language, safety_label and sample proportionally
    groups = df.groupby(["model_key", "language", "safety_label"])
    
    # Calculate how many to sample per group
    num_groups = len(groups)
    samples_per_group = max(1, args.sample_size // num_groups)
    
    sampled_dfs = []
    for g_name, g_df in groups:
        n = min(len(g_df), samples_per_group)
        sampled_dfs.append(g_df.sample(n=n, random_state=42))
        
    sampled_df = pd.concat(sampled_dfs)
    
    # If we need to top up to get exactly sample_size
    if len(sampled_df) < args.sample_size and len(sampled_df) < len(df):
        rem = df.drop(sampled_df.index)
        n_more = min(len(rem), args.sample_size - len(sampled_df))
        sampled_df = pd.concat([sampled_df, rem.sample(n=n_more, random_state=42)])

    # Output candidate list
    candidates_file = config.RESULTS_SCORED_DIR / "manual_audit_candidates.csv"
    sampled_df.to_csv(candidates_file, index=False)
    print(f"Created manual audit candidate list at {candidates_file} with {len(sampled_df)} records.")

    # Create manual review file layout (with empty manual_label for the auditor to fill)
    review_df = pd.DataFrame()
    review_df["run_id"] = sampled_df["run_id"]
    review_df["prompt_id"] = sampled_df["prompt_id"]
    review_df["model_key"] = sampled_df["model_key"]
    review_df["language"] = sampled_df["language"]
    review_df["safety_label"] = sampled_df["safety_label"]
    review_df["output_text"] = sampled_df["output_text"]
    review_df["auto_label"] = sampled_df["auto_label"]
    review_df["manual_label"] = "" # Left blank for manual review
    review_df["manual_reviewer"] = "patrick_self_audit"
    review_df["review_mode"] = "solo_delayed_blind"
    review_df["notes"] = ""

    review_file = config.RESULTS_SCORED_DIR / "manual_review.csv"
    review_df.to_csv(review_file, index=False)
    print(f"Created manual review template at {review_file}. Go ahead and review this file manually later!")

if __name__ == "__main__":
    main()
