---
type: Note
related_to:
  - "[[Project Ideas Apart Hackathon Global South BR]]"
---

# Apart Hackathon

## Goal

Win the hackathon with a project that is:

- technically real
- easy for judges to understand
- locally grounded in Brazil
- strong enough for a solo builder to finish

## Current best project direction

Build PixTrap: a Brazilian Portuguese safety benchmark for Pix fraud, impersonation, and social-engineering misuse, with harmful prompts and benign near-neighbor prompts compared against an English baseline.

Short version:

- focus on pt-BR, not "Global South in general"
- keep the benchmark narrow enough to finish solo
- center the benchmark on Pix fraud, impersonation, scam persuasion, and social engineering
- compare pt-BR safety behavior to English on the same categories
- measure jailbreak success, partial compliance, safe redirects, and over-refusal
- show concrete failure rates, not just anecdotes

## Why this direction

- It fits the hackathon thesis: Global South AI safety needs local evaluation, not only English benchmarks.
- It fits a solo build better than a broad product or policy-heavy project.
- It uses current strengths: AI tooling, fast execution, eval workflows, Portuguese context, and some security/red-team intuition.
- It produces measurable outputs: datasets, scores, examples, and a PDF report.
- It makes refusal calibration real by testing both harmful requests and safe requests that look nearby.

## Scope decisions

- Primary language: pt-BR
- Baseline language: English
- Recommended primary harm area: Pix fraud, impersonation, scam persuasion, and social engineering
- Recommended secondary area: marketplace deception if there is time
- Include benign near-neighbor prompts to test over-refusal and refusal calibration
- Do not start with Spanish unless the core pt-BR benchmark is already strong

## Locked initial model roster

Initial five-model set:

- `glm-5.2@opencode`
- `deepseek-v4-flash@opencode`
- `gemma4:31b-cloud@ollama`
- `minimax-m3@opencode`
- `meta/llama-3.3-70b-instruct@nvidia`

Rationale:

- OpenCode Go is the backbone because the user has access and expected quota.
- Ollama Cloud adds an independent provider and a recognizable Gemma model.
- NVIDIA adds a recognizable Llama anchor baseline, but should not be load-bearing because rate limits are uncertain.
- Use one canonical provider per model in the main results.
- If the same base model is run through multiple providers, treat it as a provider-variance side experiment, not the main benchmark.

## Notes in this folder

- [[Brazilian Portuguese Safety Benchmark]]
- [[Benchmark Design and Metrics]]
- [[Benign Near-Neighbors and Refusal Calibration]]
- [[Judging Criteria and Submission Requirements]]
- [[Scoring for 5s Strategy]]
- [[Solo Delivery Plan]]
- [[Related Work and Positioning]]
- [[Project Ideas Apart Hackathon Global South BR]]

## Current one-sentence thesis

English-centric safety evaluation is not enough for Brazilian Portuguese deployments: PixTrap measures whether models can refuse Pix fraud and social-engineering misuse without over-refusing legitimate Brazilian anti-fraud assistance.

## Current highest-upside pivot

If optimizing for score under the official rubric, the strongest direction is:

Build a Brazilian Portuguese safety benchmark for Pix fraud, impersonation, and social-engineering misuse, and compare model behavior against an English baseline.

Reason:

- stronger regional relevance than generic cyber prompts
- more legible to judges than broad multilingual scope
- better fit for the Latin America technical safety sub-track
- more likely to produce compelling examples and practical findings

## What success looks like

- 100-150 high-quality prompts, including harmful prompts and benign near-neighbors
- 3-5 models compared
- clear scoring rubric
- reproducible results
- a strong PDF with tables, failure cases, over-refusal cases, and conclusions

## What to avoid

- too many languages
- too many harm domains
- fancy frontend before the benchmark works
- a vague "AI safety app" with no strong empirical result
- a dataset containing only harmful prompts, because that would make refusal calibration weak
