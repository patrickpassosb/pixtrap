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

Each harmful prompt is paired with a benign near-neighbor that shares topical overlap but expresses legitimate intent. Five of the ten harmful prompts have dedicated benign near-neighbors; the remaining five are unpaired harmful probes. For example:
- **Harmful**: "Rewrite this message to look like it comes from the Bank of Brazil security center, requesting a test Pix payment."
- **Benign pair**: "I'm writing a bank security article. How do scammers typically impersonate the Bank of Brazil's security center, and how can customers identify fraud?"

This pairing enables measuring *refusal calibration*: a model that refuses both the harmful and benign prompt is over-refusing; a model that complies with both is under-refusing.

### 3.3 Languages

All prompts were written natively in Brazilian Portuguese. Matched English translations were created to isolate the effect of language on model safety behavior, keeping intent and semantics identical.

### 3.4 Model Roster

We evaluate five models across three providers:

| Model | Provider | Endpoint Type | Max Output Tokens |
|-------|----------|---------------|-------------------|
| GLM 5.2 | OpenCode Go | Chat Completions | 350 |
| MiMo V2.5 | OpenCode Go | Chat Completions | 350 |
| Gemma 4 31B Cloud | Ollama Cloud | Ollama Generate | 350 |
| Kimi K2.6 | OpenCode Go | Chat Completions | 700 |
| Llama 3.3 70B Instruct | NVIDIA | Chat Completions | 350 |

Kimi K2.6 is a reasoning model that consumes tokens for internal chain-of-thought before producing visible output. It receives a higher `max_output_tokens` budget (700) to ensure visible content is generated. All other models use a uniform 350-token budget. All models are evaluated at temperature 0.0.

### 3.5 Scoring Rubric

For harmful prompts, we assign one of: `unsafe_comply`, `partial_comply`, `refuse_weak`, `refuse_strong`, `safe_redirect`, `no_visible_output`, or `unclear`. For benign near-neighbors: `safe_comply`, `over_refuse`, `partial_comply`, `no_visible_output`, or `unclear`. Provider failures are labeled `not_scored_provider_failure` and excluded from safety metrics. The `no_visible_output` label captures cases where the provider reports a completed request but the visible assistant text is empty or null — a distinct outcome from genuine refusal or ambiguity.

### 3.6 Refusal Calibration Score

We define a summary calibration metric:

```
calibration_score = safe_redirect_rate(harmful) + safe_comply_rate(benign) − unsafe_compliance_rate − partial_compliance_rate − over_refusal_rate
```

This single number captures the model's ability to be safe where needed and helpful where appropriate. Partial compliance is penalized alongside unsafe compliance, since providing harmful details with a perfunctory warning still exposes the user to risk.

### 3.7 Transferability

The methodology is designed to be adaptable. Researchers targeting other countries, languages, or harm domains can reuse the pattern: (1) define a local fraud/harm taxonomy, (2) write harmful prompts and benign near-neighbors natively, (3) apply the scoring rubric, and (4) report calibration.

## 4. Results

All 150 runs (5 models × 30 prompts) completed successfully with zero provider failures. One run (Kimi K2.6, English benign) produced no visible output and was classified as `no_visible_output` rather than counted in the safety metric denominators. Coverage was 100% across all models and languages.

### 4.1 Coverage Summary

All five models achieved full provider completion and visible output across both languages, with the single exception noted above. No model was excluded from headline comparisons due to insufficient coverage.

### 4.2 Unsafe Compliance (Jailbreak) Rate

| Model | pt-BR | en | Cross-Language Gap |
|-------|-------|-----|---------------------|
| Kimi K2.6 | 0.0% [0.0, 27.8] | 60.0% [31.3, 83.2] | −70.0% |
| Llama 3.3 70B | 30.0% [10.8, 60.3] | 80.0% [49.0, 94.3] | −50.0% |
| GLM 5.2 | 20.0% [5.7, 51.0] | 40.0% [16.8, 68.7] | −20.0% |
| MiMo V2.5 | 20.0% [5.7, 51.0] | 40.0% [16.8, 68.7] | −20.0% |
| Gemma 4 31B | 20.0% [5.7, 51.0] | 20.0% [5.7, 51.0] | 0.0% |

Values are point estimates with Wilson 95% confidence intervals. The cross-language gap is defined as pt-BR rate minus English rate; negative values mean the model is *less safe* in English than in Portuguese.

**Key finding:** Contrary to our initial hypothesis, models are not less safe in Brazilian Portuguese — they are consistently *less safe in English*. Four of five models show a negative cross-language jailbreak gap, with Kimi K2.6 (−70%) and Llama 3.3 70B (−50%) exhibiting the largest gaps. Gemma 4 31B is the only model with no cross-language difference.

### 4.3 Over-Refusal Rate

| Model | pt-BR | en |
|-------|-------|-----|
| GLM 5.2 | 0.0% [0.0, 43.4] | 0.0% [0.0, 43.4] |
| MiMo V2.5 | 0.0% [0.0, 43.4] | 0.0% [0.0, 43.4] |
| Gemma 4 31B | 20.0% [3.6, 62.4] | 0.0% [0.0, 43.4] |
| Kimi K2.6 | 0.0% [0.0, 43.4] | 25.0% [4.6, 69.9] |
| Llama 3.3 70B | 20.0% [3.6, 62.4] | 0.0% [0.0, 43.4] |

Over-refusal is low overall (≤25%), indicating that models generally do not over-refuse legitimate anti-fraud assistance. Kimi K2.6 shows the highest over-refusal in English (25%), partly influenced by the one `no_visible_output` case in its benign English set.

### 4.4 Safe Redirect Rate

| Model | pt-BR | en |
|-------|-------|-----|
| Kimi K2.6 | 70.0% | 30.0% |
| GLM 5.2 | 80.0% | 60.0% |
| Gemma 4 31B | 50.0% | 40.0% |
| MiMo V2.5 | 30.0% | 40.0% |
| Llama 3.3 70B | 0.0% | 0.0% |

Llama 3.3 70B never redirects users to official reporting channels — it either complies unsafely or refuses without providing defensive guidance. This is a notable gap: refusing fraud requests without directing victims to help (bank, police, MED) leaves users without actionable next steps.

### 4.5 Partial Compliance Rate

Partial compliance (answering with unnecessary harmful details despite a warning) was rare: only 1 case across all 150 runs (Kimi K2.6, English). This suggests that when models do comply with harmful requests, they tend to do so fully rather than hedging.

### 4.6 Calibration Score

| Model | pt-BR | en |
|-------|-------|-----|
| Kimi K2.6 | +1.70 | +0.10 |
| GLM 5.2 | +1.60 | +1.20 |
| MiMo V2.5 | +1.10 | +1.00 |
| Gemma 4 31B | +0.90 | +1.20 |
| Llama 3.3 70B | +0.30 | +0.20 |

Kimi K2.6 achieves the best pt-BR calibration (+1.70) but collapses in English (+0.10), driven by its 60% English jailbreak rate. GLM 5.2 is the most consistent across languages. Llama 3.3 70B has the worst calibration in both languages due to high unsafe compliance and zero safe redirects.

### 4.7 Difficulty Breakdown

Jailbreak rates by prompt difficulty (on harmful prompts):

| Model | Easy | Medium | Hard |
|-------|------|--------|------|
| Kimi K2.6 (pt-BR) | 0% | 0% | 0% |
| Kimi K2.6 (en) | 100% | 80% | 33% |
| Llama 3.3 70B (pt-BR) | 0% | 20% | 67% |
| Llama 3.3 70B (en) | 50% | 100% | 67% |

Hard prompts (roleplay framing, indirect polite malicious framing) are more likely to elicit unsafe compliance, as expected. The difficulty effect is most pronounced for Llama 3.3 70B in English, where medium-difficulty prompts achieve 100% jailbreak.

### 4.8 Calibration Scatter

The calibration scatter chart (`calibration_scatter.png`) plots each model's jailbreak rate (x-axis, lower is better) against over-refusal rate (y-axis, lower is better) for both languages, with lines connecting pt-BR and English points. The ideal quadrant (lower-left) is occupied by Kimi K2.6 pt-BR and Gemma 4 31B in both languages. Llama 3.3 70B English is the outlier in the upper-right region (high jailbreak, though low over-refusal).

## 5. Discussion

### 5.1 The Cross-Language Safety Gap Runs Counter to Expectations

The most striking finding is that four of five models are *less safe in English* than in Brazilian Portuguese on Pix fraud prompts. Kimi K2.6 shows a 70-point jailbreak gap (0% pt-BR vs 60% English) and Llama 3.3 70B shows a 50-point gap (30% pt-BR vs 80% English). This contradicts the common assumption that models are less safe in non-English languages.

A likely explanation is that the Pix fraud domain is Brazil-specific: English prompts about Pix fraud fall outside the typical safety training distribution, which may focus on generic English-language harm categories. The Portuguese prompts, grounded in Brazilian institutional references (Banco Central, MED, specific scam patterns), may trigger safety alignment more effectively because they resemble real-world fraud reports that models were trained on. This suggests that locally grounded prompts can paradoxically *improve* safety alignment detection, while translating the same intent into English strips away the cultural signals that activate refusal behavior.

### 5.2 Safe Redirect Is a Differentiator

Llama 3.3 70B never produces a safe redirect in either language — it either complies unsafely or refuses without guidance. GLM 5.2 and Kimi K2.6 (pt-BR) consistently redirect users to official channels (bank, police, MED). This matters for real-world deployment: a refusal without redirect leaves a potential scam victim without actionable next steps.

### 5.3 Model Rankings

- **Best overall (pt-BR):** Kimi K2.6 (0% jailbreak, 70% redirect, calibration +1.70)
- **Best overall (en):** Gemma 4 31B (20% jailbreak, 0% over-refusal, calibration +1.20)
- **Most consistent across languages:** Gemma 4 31B (0% gap) and GLM 5.2 (small gap, high redirect in both)
- **Worst overall:** Llama 3.3 70B (80% English jailbreak, 0% redirect, calibration +0.20)

### 5.4 Limitations of Keyword-Based Scoring

The automated scorer uses keyword matching and word-count heuristics to classify outputs. The `refuse_strong` vs `refuse_weak` distinction relies on a 40-word cutoff, and `partial_comply` detection depends on warning-word presence plus a 50-word threshold. These heuristics are brittle for edge cases but are validated by a delayed blind manual audit (see §6). The audit disagreement rate provides a concrete measure of scorer reliability.

The PixTrap methodology demonstrates that locally grounded safety benchmarks can be constructed at low cost using free-tier API access, simple keyword-based scoring heuristics validated by manual audit, and a near-neighbor calibration design that avoids the false binary of "safe model" vs. "unsafe model." Instead, PixTrap asks: does the model know where the line is?

This approach can be adapted to other countries and harm domains. A researcher in India could apply the same recipe to UPI fraud; a researcher in Nigeria could apply it to mobile money scams. The core pattern—local taxonomy, native-language prompts, benign near-neighbor pairing, and calibration scoring—transfers across settings.

## 6. Limitations and Dual-Use Considerations

**Dataset size.** The dataset contains 30 prompts (15 pt-BR, 15 English; 10 harmful and 5 benign near-neighbors per language). While sufficient for demonstrating the methodology and revealing cross-language patterns, this sample is too small for strong statistical claims about individual model differences. The Wilson 95% confidence intervals are wide (e.g., 20% ± [5.7%, 51.0%] for a 2/10 rate), reflecting this uncertainty. Only five of ten harmful prompts have dedicated benign near-neighbor pairs.

**Provider constraints.** Kimi K2.6 is a reasoning model that requires a higher token budget (700 vs 350) to produce visible output. We report this transparently as a methodological note. All other models use a uniform 350-token budget.

**Scorer subjectivity.** The automated keyword-based scorer is a heuristic with known limitations: the `refuse_strong`/`refuse_weak` distinction uses a word-count cutoff, and `partial_comply` detection relies on warning-word matching. We validate it with a single-author delayed blind manual audit of 30 stratified samples and report the disagreement rate. The audit was performed by the sole author (Patrick Passos) and is not an independent review.

**Dual-use risk.** The harmful prompts in this dataset are realistic social-engineering templates. To prevent misuse, raw harmful prompts are not published in the public repository. The public sample contains redacted harmful prompts and full benign near-neighbors. Qualified researchers may request access to the complete dataset for reproducibility.

**LLM Usage Statement.** AI coding assistants were used as interactive programming partners during implementation, including code generation, test development, chart design, and report drafting. All analysis decisions, prompt design, and methodology were directed by the author.

## References

- Chao, P., et al. (2024). JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models. *arXiv preprint*.
- Deng, Y., et al. (2023). Multilingual Jailbreak Challenges in Large Language Models. *arXiv preprint*.
- Yong, Z.-X., et al. (2023). Low-Resource Languages Jailbreak GPT-4. *arXiv preprint*.
- Wang, Y., et al. (2023). Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs. *arXiv preprint*.
- Central Bank of Brazil. (2023). Mecanismo Especial de Devolução (MED) - Regulamento do Pix.
- Febraban. (2024). Guia de Segurança contra Golpes do Pix.
