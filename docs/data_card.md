# PixTrap Data Card

This data card provides metadata and overview of the PixTrap dataset.

## Dataset Overview
- **Name**: PixTrap (Brazilian Portuguese Pix Fraud Safety Benchmark)
- **Version**: 0.1.0 (Pilot)
- **Languages**: Brazilian Portuguese (`pt-BR`), English (`en`)
- **Format**: JSONL (JSON Lines), one prompt record per line.
- **Licensing**: Open for research, gated raw harmful prompts.

## Taxonomy and Size
The pilot dataset contains **30 prompts** total:
- **pt-BR Set (15 prompts)**:
  - 10 Harmful (impersonation, urgency coercion, transaction receipt fraud, recovery support scams)
  - 5 Benign Near-Neighbors (education, victim support, consumer protection, bank compliance)
- **English Set (15 prompts)**:
  - 10 Matched Harmful
  - 5 Matched Benign Near-Neighbors

## Pairing Logic
We pair harmful prompts with benign near-neighbors using a `paired_with` field. This enables measuring **over-refusal** on legitimate anti-fraud topics. A model is well-calibrated if it refuses the harmful prompts (expected behavior: `refuse_and_redirect`) and complies with the benign near-neighbors (expected behavior: `comply_safely`).

## Public Release Limitations & Dual-Use Context
- The raw harmful prompt text is **dual-use**: it contains realistic social-engineering patterns that could be used for malicious purposes if released carelessly.
- To balance reproducibility with security, the repository contains:
  1. A **sanitized sample dataset** (`data/sample_prompts_public.jsonl`) with redacted harmful prompts.
  2. A **gated policy** for researcher access to raw harmful prompts.
- All evaluation runs should be performed with the local, complete datasets (`data/prompts_ptbr.jsonl` and `data/prompts_en.jsonl`) but these should not be pushed to public public repositories.
