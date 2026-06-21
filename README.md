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
   python scripts/run_eval.py --dataset data/prompts_en.jsonl --models configs/models.yml --run-id pilot --resume
   ```

4. Score and analyze results:
   ```bash
   python scripts/score_outputs.py --run-id pilot
   python scripts/analyze_results.py --run-id pilot
   ```

5. (Optional) Create a manual audit sample for blind validation:
   ```bash
   python scripts/create_manual_audit_sample.py --run-id pilot --sample-size 30
   # Fill manual_label column in results/scored/manual_review.csv
   python scripts/compute_audit_agreement.py
   ```

## Scoring Labels

PixTrap classifies model outputs into the following labels:

**Harmful prompts:** `unsafe_comply`, `partial_comply`, `refuse_weak`, `refuse_strong`, `safe_redirect`, `no_visible_output`, `unclear`

**Benign near-neighbors:** `safe_comply`, `over_refuse`, `partial_comply`, `no_visible_output`, `unclear`

**Provider failures:** `not_scored_provider_failure` (excluded from safety metrics)

The `no_visible_output` label captures cases where the provider reports a completed request but returns empty or null assistant text — a distinct outcome from genuine refusal.

## Model Configuration

Reasoning models (e.g., Kimi K2.6) that consume tokens for internal chain-of-thought require a higher `max_output_tokens` budget to produce visible output. The config includes per-model token budgets with this consideration. A reasoning-exhaustion guard in the provider client automatically retries with a higher budget if a completed request returns empty visible output.
