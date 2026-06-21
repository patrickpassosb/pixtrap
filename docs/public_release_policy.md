# PixTrap Public Release Policy

This document outlines the policy for distributing the PixTrap benchmark and its associated datasets to balance scientific reproducibility with AI safety and dual-use risk management.

## Risk Assessment
The PixTrap dataset contains realistic Brazilian Portuguese social-engineering templates (fake bank messages, urgency scripts, fake kidnapping scripts). Although these are framed as LLM prompts, they are highly actionable. If compiled into a single public repository, they could function as a "scam template package" for malicious actors.

## Distribution Policy

### Publicly Accessible Artifacts:
- **Benchmark Code**: Evaluator scripts, provider adapters, resume logic, analysis code.
- **Scoring Rubric & Guidelines**: Rules for manual audit and automated classifiers.
- **Aggregated Results & Analysis**: Metrics, confidence intervals, comparison charts.
- **Sanitized Public Dataset**: `data/sample_prompts_public.jsonl` contains the exact schema and the full text of benign prompts, but has redacted text for the harmful prompts.
- **Taxonomy & Sourcing Documentation**: Detailed descriptions of the fraud mechanisms evaluated.

### Gated/Redacted Artifacts:
- **Raw Harmful Prompt Files**: `data/prompts_ptbr.jsonl` and `data/prompts_en.jsonl` are kept out of public repositories.
- **Scam Templates**: Screenshots, presentations, and slides must not display the unredacted text of the most effective harmful prompts.
- **Final Report**: The PDF report may include brief, heavily redacted or abstracted examples of harmful prompts but must not print complete actionable scam texts.

## Access Requests for Researchers
Researchers wishing to reproduce PixTrap results or run the benchmark on their own models can request access to the complete, unredacted datasets.
To request access, please contact the author (`patrick_self_audit` / project maintainer) with:
1. Proof of institutional or corporate affiliation.
2. A brief statement of the intended research use.
3. Agreement not to republish the raw harmful prompts.
