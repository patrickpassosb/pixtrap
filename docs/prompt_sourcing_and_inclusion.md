# Prompt Sourcing and Inclusion Criteria

This document explains the origins of the prompts in the PixTrap dataset, how they were curated, and the logic behind their inclusion or exclusion.

## Taxonomy Sourcing
The PixTrap taxonomy was designed based on real-world Brazilian fraud patterns. The primary categories are:
1. **Impersonation and False Authority**: Masquerading as bank support, police, or contacts.
2. **Urgency and Coercion**: Fake kidnapping, immediate bill cutoffs.
3. **Transaction Receipt Fraud**: Fake payment receipts and altered metadata.
4. **Recovery and Support Scams**: Fake "Pix bug" recovery systems.
5. **Benign Near-Neighbors**: Legitimate requests related to anti-fraud education, support, and compliance.

These categories were derived from:
- Public anti-fraud guidance from Brazilian financial institutions (e.g., Febraban, Banco do Brasil, Itaú).
- Official communications from the Central Bank of Brazil (BCB) regarding common Pix scams and the Mecanismo Especial de Devolução (MED).
- Brazilian consumer-protection reports (Procon) and news reports on social-engineering attacks.

## Prompt Drafting and Translation
- **Native Drafting**: The `pt-BR` prompts were written natively in Brazilian Portuguese to ensure they use authentic terminology (e.g., "central de segurança", "gerente de conta", "sequestro falso", "agendamento Pix").
- **English Matching**: Matched English prompts in `prompts_en.jsonl` were translated from the native `pt-BR` templates to isolate the effect of language on model refusal behavior, keeping intent and semantics identical.

## Harmful / Benign Pairing
To evaluate calibration (distinguishing harmful intent from legitimate safety-related inquiries), harmful prompts are paired with "benign near-neighbors". For example:
- **Harmful**: Asking the model to rewrite a message to impersonate bank security asking for a Pix test.
- **Benign Pair**: Asking the model to explain how scammers impersonate bank security and how customers can defend themselves.

## Inclusion & Exclusion Criteria

### Inclusion Criteria:
- Must fit one of the five taxonomy categories.
- Must represent realistic Brazilian Portuguese social-engineering context (e.g., mentioning specific banks, local utility companies like Enel, or local tools like MED).
- Must have a clear and unambiguous safety label.

### Exclusion Criteria:
- Prompts that are too generic to be relevant to Pix or Brazilian contexts.
- Prompts containing actionable, highly optimized code or exploit scripts that present direct safety risks (e.g., full phishing email drafts with actual malicious links).
- Duplicates or minor stylistic variations that do not add taxonomy coverage.
