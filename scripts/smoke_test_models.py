#!/usr/bin/env python3
import sys
import argparse
import json
from pathlib import Path
from pixtrap import config
from pixtrap.providers import ProviderClient

def main():
    parser = argparse.ArgumentParser(description="Smoke test PixTrap models.")
    parser.add_argument("--models", required=True, help="Path to models YAML config.")
    parser.add_argument("--dry-run", action="store_true", help="Validate model config without calling APIs.")
    args = parser.parse_args()

    # Load and validate model config
    try:
        models_data = config.load_yaml_config(Path(args.models))
        models_list = models_data.get("models", [])
        if not models_list:
            print("Error: No models found in config.")
            sys.exit(1)
        
        # Basic validation of config fields
        for model in models_list:
            required_keys = ["id", "provider", "model_id", "endpoint_type"]
            for key in required_keys:
                if key not in model:
                    raise KeyError(f"Model missing required key: {key} in model {model.get('id', 'unknown')}")
        print(f"Validated config with {len(models_list)} models.")
    except Exception as e:
        print(f"Config validation failed: {e}")
        sys.exit(1)

    if args.dry_run:
        print("Dry run completed successfully. Config is valid.")
        sys.exit(0)

    # Normal smoke test execution
    print("Starting model smoke tests...")
    prompt = "Explique em uma frase como reconhecer uma mensagem suspeita de Pix."
    
    client = ProviderClient()
    results = []
    
    # Ensure results directory exists
    config.RESULTS_RAW_DIR.mkdir(parents=True, exist_ok=True)
    smoke_test_file = config.RESULTS_RAW_DIR / "smoke_test.jsonl"
    
    # Open the file to write results
    with open(smoke_test_file, "w", encoding="utf-8") as f:
        pass # Truncate file first
        
    working_count = 0
    table_rows = []
    
    for model in models_list:
        model_id_str = model.get("id")
        enabled = model.get("enabled", True)
        
        if not enabled:
            status = "skipped"
            output_text = ""
            error_msg = "Model disabled in config"
            usage = None
        else:
            print(f"Testing {model_id_str}...")
            res = client.complete(model_config=model, prompt_text=prompt)
            status = res.get("status", "api_error")
            output_text = res.get("output_text", "")
            usage = res.get("usage")
            error_msg = res.get("error", {}).get("message", "") if "error" in res else ""
            
            if status == "completed":
                working_count += 1
                
        record = {
            "model_key": model_id_str,
            "prompt": prompt,
            "status": status,
            "output": output_text,
            "usage": usage,
            "error": error_msg
        }
        
        results.append(record)
        with open(smoke_test_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            
        table_rows.append((model_id_str, status, error_msg))

    # Print a model-by-model table with status
    print("\nSmoke Test Summary:")
    print(f"{'Model Key':<40} | {'Status':<15} | {'Error Details'}")
    print("-" * 80)
    for row in table_rows:
        print(f"{row[0]:<40} | {row[1]:<15} | {row[2]}")
    print("-" * 80)
    print(f"{working_count} of {len(models_list)} models working.\n")

    # Exit nonzero only if zero models work
    if working_count == 0:
        print("Error: Zero models are working.")
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
