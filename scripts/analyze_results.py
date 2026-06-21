#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
from pixtrap import config
from pixtrap.analysis import analyze_scored_results
from pixtrap.charts import generate_evaluation_charts

def main():
    parser = argparse.ArgumentParser(description="Analyze PixTrap scored results and plot charts.")
    parser.add_argument("--run-id", required=True, help="Run ID of the evaluation to analyze.")
    args = parser.parse_args()

    scored_csv = config.RESULTS_SCORED_DIR / f"results_{args.run_id}_scored.csv"
    if not scored_csv.exists():
        print(f"Error: Scored CSV file {scored_csv} does not exist. Run scoring first.")
        sys.exit(1)

    print(f"Analyzing scored results from {scored_csv}...")
    cov_df, unc_df = analyze_scored_results(scored_csv)

    # Save summary tables
    cov_file = config.RESULTS_SCORED_DIR / "coverage_summary.csv"
    unc_file = config.RESULTS_SCORED_DIR / "uncertainty_summary.csv"
    
    cov_df.to_csv(cov_file, index=False)
    unc_df.to_csv(unc_file, index=False)
    
    print(f"Saved coverage summary to {cov_file}")
    print(f"Saved uncertainty/metrics summary to {unc_file}")

    print("\nGenerating charts...")
    generate_evaluation_charts(scored_csv, config.RESULTS_CHARTS_DIR)

    # Print summary tables to stdout
    print("\nCoverage Summary Table:")
    print(cov_df.to_string(index=False))

    print("\nKey Metrics Summary Table:")
    # Filter for headline metrics to print clearly
    print(unc_df.to_string(index=False))

if __name__ == "__main__":
    main()
