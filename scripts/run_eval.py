#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
from pixtrap import config
from pixtrap.dataset import load_dataset
from pixtrap.runner import EvaluationRunner

def main():
    parser = argparse.ArgumentParser(description="Run PixTrap safety evaluation.")
    parser.add_argument("--dataset", help="Path to prompts JSONL file. Optional if resuming.")
    parser.add_argument("--models", help="Path to models YAML config. Optional if resuming.")
    parser.add_argument("--run-id", required=True, help="Unique identifier for the evaluation run.")
    parser.add_argument("--resume", action="store_true", help="Resume from an existing incomplete run.")
    parser.add_argument("--force", action="store_true", help="Force run all pairs even if already completed.")
    args = parser.parse_args()

    # Determine dataset and models paths
    dataset_path = args.dataset
    models_path = args.models

    if not args.resume:
        if not dataset_path:
            print("Error: --dataset is required for new runs.")
            sys.exit(1)
        if not models_path:
            print("Error: --models is required for new runs.")
            sys.exit(1)
    else:
        # Defaults if resuming
        if not dataset_path:
            # We check if prompts_ptbr exists, or we ask
            dataset_path = "data/prompts_ptbr.jsonl"
            print(f"Resuming: --dataset not provided. Defaulting to {dataset_path}")
        if not models_path:
            models_path = "configs/models.yml"
            print(f"Resuming: --models not provided. Defaulting to {models_path}")

    # Verify files exist
    if not Path(dataset_path).exists():
        print(f"Error: Dataset path {dataset_path} does not exist.")
        sys.exit(1)
    if not Path(models_path).exists():
        print(f"Error: Models config path {models_path} does not exist.")
        sys.exit(1)

    print(f"Loading dataset: {dataset_path} ...")
    prompts = load_dataset(dataset_path)
    print(f"Loaded {len(prompts)} prompts.")

    print(f"Loading models: {models_path} ...")
    models_config_data = config.load_yaml_config(Path(models_path))
    models_list = models_config_data.get("models", [])
    print(f"Loaded {len(models_list)} models from config.")

    # Initialize runner and run
    runner = EvaluationRunner(
        run_id=args.run_id,
        model_configs=models_list,
        prompt_records=prompts,
        force=args.force,
        resume=args.resume
    )
    
    runner.run()

if __name__ == "__main__":
    main()
