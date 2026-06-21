---
type: Note
related_to: "[[Apart Hackathon]]"
---

# Scoring for 5s Strategy

## Rigid assessment

The default version of the project does not automatically score 5 in all dimensions.

Plain version:

- "We built a PT-BR benchmark for harmful prompts and tested a few models."

Likely score profile:

- Impact and innovation: 3 to 4
- Execution quality: 3 to 4
- Presentation and clarity: 4 if written well

Reason:

- multilingual safety benchmarks already exist
- jailbreak benchmarks already exist
- refusal calibration evals already exist

So a simple local-language benchmark is not enough by itself to deserve a 5 on impact and innovation.

## What has the best chance to score 5s

### Best current direction

Build a Brazilian Portuguese benchmark for Pix fraud, impersonation, and social-engineering misuse, pair harmful prompts with benign near-neighbors, and compare pt-BR safety behavior against an English baseline.

This is better than:

- generic website hacking
- broad red teaming
- broad multilingual fairness
- a pure policy memo

### Why this is stronger

- Pix is a highly legible Brazil-specific system and fraud vector.
- Social-engineering misuse is easy for judges to understand as a real deployment risk.
- It creates region-specific evidence, not just translated prompts.
- It fits the Latin America technical safety sub-track directly.
- Benign near-neighbors make refusal calibration measurable instead of rhetorical.

## How to target a 5 on Dimension 1

To approach a 5 on impact and innovation, the project must be framed as more than a benchmark.

The core claim should be:

- English-aligned safeguards do not reliably transfer to Brazilian Portuguese social-engineering patterns, especially those centered on Pix fraud and impersonation.

To strengthen novelty:

- create a Brazil-grounded taxonomy, not only prompt translations
- include attack patterns specific to trust-building and scam rewriting
- include benign near-neighbors for legitimate anti-fraud, victim-support, journalism, legal, and compliance requests
- show why these risks are neglected in current mainstream evals
- include a clear theory of change: who can use this benchmark and what decisions it enables

Best realistic target:

- 4 is realistic
- 5 is possible only if the novelty framing and evidence are excellent

## How to target a 5 on Dimension 2

Execution needs to be unusually disciplined.

Must-have elements:

- clean dataset schema
- explicit taxonomy
- carefully matched English baseline
- harmful and benign near-neighbor prompt sets
- reproducible model runs
- scoring rubric with clear labels
- spot-checked manual validation
- quantitative results plus concrete examples
- limitations clearly stated

What would weaken the score:

- too many categories
- weak prompt realism
- unclear baseline matching
- measuring only harmful prompts while claiming refusal calibration
- no validation of scoring
- conclusions that go beyond the evidence

Best realistic target:

- 4 is realistic
- 5 is possible if validation is unusually robust for a hackathon

## How to target a 5 on Dimension 3

This is the easiest dimension to control.

Must-have presentation qualities:

- a one-sentence thesis
- one figure or table that immediately shows the main finding
- a short and concrete abstract
- simple section flow
- examples that make the risk obvious
- limitations and dual-use section written clearly

The report should feel:

- sharp
- not bloated
- easy to skim
- easy to cite

Best realistic target:

- 5 is highly achievable with disciplined writing and structure

## Final strategic recommendation

Main theme:

- Pix fraud
- impersonation
- scam persuasion
- social engineering
- refusal calibration through benign near-neighbor prompts

Secondary at most:

- a small phishing or credential-theft category

Avoid as core theme:

- website hacking
- generic offensive security assistance
- too many unrelated harm domains

## Working thesis

PixTrap: a Brazilian Portuguese safety benchmark for Pix fraud, impersonation, and social-engineering misuse, using benign near-neighbors to measure refusal calibration against an English baseline.

## Hard truth

The goal should not be to assume the project is already a 5.

The goal should be:

- frame it so a 5 is arguable on impact
- execute it so a 4 to 5 is defensible on methodology
- present it so a 5 on clarity is likely
