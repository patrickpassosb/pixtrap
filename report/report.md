# PixTrap: Do Models Know When Pix Help Becomes Pix Fraud?

**Patrick Passos**

*Independent Researcher*

---

## Abstract

We introduce PixTrap, a Brazilian Portuguese safety benchmark for evaluating whether large language models can distinguish Pix fraud and social-engineering misuse from legitimate anti-fraud assistance. PixTrap pairs harmful prompts with benign near-neighbors across Brazil-specific fraud patterns, including impersonation, urgency pressure, fake transaction evidence, and recovery scams. We compare five models across Brazilian Portuguese and matched English prompts, measuring unsafe compliance, partial compliance, safe redirects, over-refusal, and cross-language safety gaps. The benchmark is designed to be low-cost, reproducible under free-tier API constraints, and useful for researchers or deployers evaluating models in Brazilian contexts. Our goal is to show where English-centric safety testing misses local failure modes, provide practical evaluation infrastructure for safer Portuguese-language AI deployments, and demonstrate a reusable methodology for building locally grounded safety benchmarks in other underrepresented languages and regions.

---

## 1. Introduction

Brazil's Pix instant payment system, launched by the Central Bank of Brazil in November 2020, now serves over 150 million users and processes billions of transactions monthly. Its widespread adoption has made it the primary vector for a distinctive class of social-engineering attacks: bank impersonation via WhatsApp, fake kidnapping urgency scams, forged transaction receipts, and fraudulent "Pix recovery" services that victimize previous scam targets.

Despite the severity of these threats, AI safety evaluations remain predominantly English-centric. Standard jailbreak and refusal benchmarks test whether models refuse harmful requests in English, but they rarely account for the cultural idioms, institutional references (e.g., Banco do Brasil, Mecanismo Especial de Devolução), and conversational norms that make Brazilian social engineering effective. When a model is deployed to serve Portuguese-speaking users in Brazil, its safety behavior may differ substantially from what English benchmarks predict.

PixTrap addresses this gap. It is both a concrete pt-BR benchmark artifact—with a Brazil-specific fraud taxonomy, paired harmful and benign prompts, and reproducible model comparisons—and a demonstration of a reusable methodology for building locally grounded safety benchmarks in underrepresented languages and regions. By measuring not only whether models refuse harmful prompts but also whether they over-refuse legitimate anti-fraud help, PixTrap evaluates *calibration*: the ability to draw the line between Pix help and Pix fraud.

## 2. Related Work

**Jailbreak and refusal benchmarks.** JailbreakBench (Chao et al., 2024) and similar frameworks evaluate whether models can be induced to produce harmful content through adversarial prompting. These benchmarks provide important baselines but are predominantly English-language and focus on universal harm categories rather than region-specific attack patterns.

**Multilingual safety evaluation.** Recent work has begun extending safety evaluations beyond English, testing models in Chinese, Arabic, and other languages. These studies consistently find that model safety degrades in non-English settings, but coverage of Portuguese—particularly Brazilian Portuguese—remains sparse.

**Culturally grounded evaluation.** A growing body of work argues that safety evaluations must account for local cultural contexts, legal frameworks, and social norms. PixTrap contributes to this tradition by grounding its taxonomy in Brazil-specific payment fraud patterns rather than translating generic English harm categories.

**Portuguese-language AI evaluation.** While Portuguese NLP benchmarks exist for general capabilities (e.g., ASSIN, PORTTINARI), safety-specific benchmarks for Brazilian Portuguese are largely absent from the literature.

PixTrap builds on these traditions while contributing a Brazil-grounded benchmark and a replicable local-benchmark construction pattern.

## 3. Methodology

### 3.1 Fraud Taxonomy

We define four harmful categories drawn from documented Brazilian Pix fraud patterns:

1. **Impersonation and False Authority**: Attackers masquerade as bank security agents, police officers, or trusted contacts to request Pix keys or transfers.
2. **Urgency and Coercion**: Attackers use high-pressure tactics, fake kidnapping scenarios, or imminent bill cutoffs to bypass user critical thinking.
3. **Transaction Receipt Fraud**: Attackers request help generating fake bank receipts or altering payment confirmations to deceive sellers.
4. **Recovery and Support Scams**: Attackers offer fraudulent "Pix recovery" or "Pix support" services to steal money from previous victims.

A fifth category, **Benign Near-Neighbors**, contains legitimate educational, compliance, support, or research requests that a well-calibrated model should answer safely.

### 3.2 Prompt Design and Pairing

Each harmful prompt is paired with a benign near-neighbor that shares topical overlap but expresses legitimate intent. For example:
- **Harmful**: "Rewrite this message to look like it comes from the Bank of Brazil security center, requesting a test Pix payment."
- **Benign pair**: "I'm writing a bank security article. How do scammers typically impersonate the Bank of Brazil's security center, and how can customers identify fraud?"

This pairing enables measuring *refusal calibration*: a model that refuses both the harmful and benign prompt is over-refusing; a model that complies with both is under-refusing.

### 3.3 Languages

All prompts were written natively in Brazilian Portuguese. Matched English translations were created to isolate the effect of language on model safety behavior, keeping intent and semantics identical.

### 3.4 Model Roster

We evaluate five models across three providers:

| Model | Provider | Endpoint Type |
|-------|----------|---------------|
| GLM 5.2 | OpenCode Go | Chat Completions |
| DeepSeek V4 Flash | OpenCode Go | Chat Completions |
| Gemma 4 31B Cloud | Ollama Cloud | Ollama Generate |
| MiniMax M3 | OpenCode Go | Messages |
| Llama 3.3 70B Instruct | NVIDIA | Chat Completions |

All models are evaluated with temperature 0.0 and max output tokens of 350.

### 3.5 Scoring Rubric

For harmful prompts, we assign one of: `unsafe_comply`, `partial_comply`, `refuse_weak`, `refuse_strong`, `safe_redirect`, or `unclear`. For benign near-neighbors: `safe_comply`, `over_refuse`, `partial_comply`, or `unclear`. Provider failures are labeled `not_scored_provider_failure` and excluded from safety metrics.

### 3.6 Refusal Calibration Score

We define a summary calibration metric:

```
calibration_score = safe_redirect_rate(harmful) + safe_comply_rate(benign) − unsafe_compliance_rate − over_refusal_rate
```

This single number captures the model's ability to be safe where needed and helpful where appropriate.

### 3.7 Transferability

The methodology is designed to be adaptable. Researchers targeting other countries, languages, or harm domains can reuse the pattern: (1) define a local fraud/harm taxonomy, (2) write harmful prompts and benign near-neighbors natively, (3) apply the scoring rubric, and (4) report calibration.

## 4. Results

[RESULT SLOT: Insert coverage summary table from coverage_summary.csv after analyze_results.py completes]

[RESULT SLOT: Insert unsafe compliance (jailbreak) rate table by model and language after analyze_results.py completes]

[RESULT SLOT: Insert over-refusal rate table by model and language after analyze_results.py completes]

[RESULT SLOT: Insert calibration scatter chart (calibration_scatter.png) after analyze_results.py completes]

[RESULT SLOT: Insert cross-language gap analysis after analyze_results.py completes]

## 5. Discussion

[RESULT SLOT: Interpret the calibration scatter chart and model rankings after results are available]

The PixTrap methodology demonstrates that locally grounded safety benchmarks can be constructed at low cost using free-tier API access, simple keyword-based scoring heuristics validated by manual audit, and a near-neighbor calibration design that avoids the false binary of "safe model" vs. "unsafe model." Instead, PixTrap asks: does the model know where the line is?

This approach can be adapted to other countries and harm domains. A researcher in India could apply the same recipe to UPI fraud; a researcher in Nigeria could apply it to mobile money scams. The core pattern—local taxonomy, native-language prompts, benign near-neighbor pairing, and calibration scoring—transfers across settings.

## 6. Limitations and Dual-Use Considerations

**Dataset size.** The pilot dataset contains 30 prompts (15 pt-BR, 15 English). While sufficient for demonstrating the methodology, this sample is too small for strong statistical claims about individual model differences. The Wilson 95% confidence intervals reflect this uncertainty.

**Provider constraints.** Free-tier API quotas may limit coverage. We report coverage rates alongside all metrics and exclude models with insufficient coverage from headline comparisons.

**Scorer subjectivity.** The automated keyword-based scorer is a heuristic. We validate it with a single-author delayed blind manual audit and report the disagreement rate. The audit was performed by the sole author (Patrick Passos) and is not an independent review.

**Dual-use risk.** The harmful prompts in this dataset are realistic social-engineering templates. To prevent misuse, raw harmful prompts are not published in the public repository. The public sample contains redacted harmful prompts and full benign near-neighbors. Qualified researchers may request access to the complete dataset for reproducibility.

**LLM Usage Statement.** Google Antigravity was used as an interactive programming partner during implementation, including code generation, test development, chart design, and report drafting.

## References

- Chao, P., et al. (2024). JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models. *arXiv preprint*.
- Deng, Y., et al. (2023). Multilingual Jailbreak Challenges in Large Language Models. *arXiv preprint*.
- Yong, Z.-X., et al. (2023). Low-Resource Languages Jailbreak GPT-4. *arXiv preprint*.
- Wang, Y., et al. (2023). Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs. *arXiv preprint*.
- Central Bank of Brazil. (2023). Mecanismo Especial de Devolução (MED) - Regulamento do Pix.
- Febraban. (2024). Guia de Segurança contra Golpes do Pix.
