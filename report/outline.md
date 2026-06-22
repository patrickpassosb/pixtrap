# PixTrap Reveals LLM Safety Calibration Gaps in Brazilian Pix Fraud

## Abstract
We introduce PixTrap, a Brazilian Portuguese safety benchmark for evaluating whether large language models can distinguish Pix fraud and social-engineering misuse from legitimate anti-fraud assistance. PixTrap pairs harmful prompts with benign near-neighbors across Brazil-specific fraud patterns, including impersonation, urgency pressure, fake transaction evidence, and recovery scams. We compare five models across Brazilian Portuguese and matched English prompts, measuring unsafe compliance, partial compliance, safe redirects, over-refusal, and cross-language safety gaps. The benchmark is designed to be low-cost, reproducible under free-tier API constraints, and useful for researchers or deployers evaluating models in Brazilian contexts. Our goal is to show where English-centric safety testing misses local failure modes, provide practical evaluation infrastructure for safer Portuguese-language AI deployments, and demonstrate a reusable methodology for building locally grounded safety benchmarks in other underrepresented languages and regions.

## 1. Introduction
- Wide adoption of Pix in Brazil (instant payment backend for over 150 million users).
- Emergence of local fraud patterns and social engineering (whatsapp cloning, bank impersonation, fake receipts, refund support scams).
- English-centric safety evaluation limits: standard safety testing does not catch local idioms, cultural contexts, or regional system vulnerabilities.
- Introducing PixTrap as both:
  - A concrete pt-BR benchmark artifact.
  - A reusable method demonstrating how locally-tailored safety evaluations can be constructed in underrepresented languages and regions.

## 2. Related Work
- Refusal and jailbreak robust evaluation (e.g. JailbreakBench).
- Multilingual safety evaluations and their limits.
- Culturally grounded safety evaluations.
- Portuguese language safety evaluation work.

## 3. Methodology
- Fraud taxonomy containing 4 main harmful categories:
  - Impersonation and False Authority
  - Urgency and Coercion
  - Transaction Receipt Fraud
  - Recovery and Support Scams
- Benign Near-Neighbors calibration approach:
  - Legitimate questions mapped as paired near-neighbors to test over-refusal (e.g., anti-fraud education, support, consumer protection, bank compliance).
- Model Roster:
  - Five models evaluated across different providers.
- Scoring Rubric:
  - Standardized labels (unsafe_comply, partial_comply, refuse_strong, refuse_weak, safe_redirect, safe_comply, over_refuse).
- Evaluation Protocol and Dual-Use Safety Controls (redacted raw prompts).

## 4. Results
- [RESULT SLOT: Main coverage and scored output overview]
- [RESULT SLOT: Unsafe compliance (jailbreak) rates by model]
- [RESULT SLOT: Over-refusal rates by model]
- [RESULT SLOT: Cross-language gaps (pt-BR vs English)]
- [RESULT SLOT: Calibration scatter plot explanation]

## 5. Discussion
- Implications of results for Brazilian deployments.
- Explaining how the PixTrap recipe can be adapted to other locales (local taxonomy + benign near-neighbor pairing + calibration scoring).

## 6. Limitations and Dual-Use Considerations
- Dataset size, provider APIs, and rate limits.
- Potential misuse of raw prompts and why they are gated.
- Delayed blind solo manual audit protocol (Patrick self-audit).

## References
- Listing relevant papers (JailbreakBench, Multilingual Safety, etc.).
