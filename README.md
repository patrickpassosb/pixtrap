# PixTrap

**PixTrap: Do Models Know When Pix Help Becomes Pix Fraud?**

PixTrap is a Brazilian Portuguese safety benchmark that evaluates whether language models refuse Pix fraud, impersonation, and social-engineering misuse while still answering legitimate anti-fraud help requests.

English-centric safety evaluation is not enough for Brazilian Portuguese deployments: PixTrap measures whether models can refuse Pix fraud and social-engineering misuse without over-refusing legitimate Brazilian anti-fraud assistance.

## Installation

This project uses `uv` to manage dependencies and virtual environments.

To set up the project:
```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Running the Benchmark

1. Configure your `.env` file with the required API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your keys
   ```

2. Run the pre-run verification (smoke tests):
   ```bash
   python scripts/smoke_test_models.py --models configs/models.yml
   ```

3. Run the evaluations:
   ```bash
   python scripts/run_eval.py --dataset data/prompts_ptbr.jsonl --models configs/models.yml --run-id pilot
   python scripts/run_eval.py --dataset data/prompts_en.jsonl --models configs/models.yml --run-id pilot
   ```

4. Score and analyze results:
   ```bash
   python scripts/score_outputs.py --run-id pilot
   python scripts/analyze_results.py --run-id pilot
   ```
