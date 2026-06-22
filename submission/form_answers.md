# Apart Hackathon Submission Form Answers

- **Project Title**: PixTrap Reveals LLM Safety Calibration Gaps in Brazilian Pix Fraud
- **Project Summary (Max 150 words)**:
  PixTrap is a Brazilian Portuguese safety benchmark that evaluates whether large language models can refuse Pix fraud, impersonation, and urgency-based social engineering while still answering legitimate anti-fraud help requests. Standard English-centric safety evaluations fail to capture regional Portuguese idioms, local financial institutions (e.g., Central Bank of Brazil, Banco do Brasil), and instant payment architectures (Pix). By pairing harmful prompts with benign near-neighbors, PixTrap measures both unsafe compliance and over-refusal. Evaluated across five models in pt-BR and English, our results reveal a modest cross-language safety gap (10-20% less safe in English for 3 of 5 models) and uncover a methodological insight: keyword-based scoring can create artificial cross-language gaps if refusal patterns are not language-aware. PixTrap offers a lightweight, reproducible evaluation package and demonstrates a reusable local-safety benchmark construction recipe for underrepresented regions.
- **Track Selection**: Latin America (Regional) + Technical Safety (Sub-track)
- **Publishing Interest**: Yes, we intend to publish or present this benchmark to help improve local LLM deployments.
- **Team Name**: PixTrap Team
- **Location**: Brazil
- **Team Members**:
  - Name: Patrick Passos
  - Email: patrick.passos@example.com (replace with user email)
  - Discord Username: patrick_passos
  - Google Scholar: N/A
- **Code Repository**: https://github.com/patrickpassosb/pixtrap
- **Additional Material**: https://github.com/patrickpassosb/pixtrap (public sample dataset, full code, results, charts)
- **Dual-Use / Safety Redaction Note**: 
  To prevent this repository from serving as a source of optimized scam templates, we do not release the raw harmful prompts publicly. The public repository includes the complete evaluation code, scoring criteria, and a sanitized public sample dataset (`data/sample_prompts_public.jsonl`) with redacted harmful prompt content. Researchers can request access to the unredacted evaluation sets for validation purposes by contacting the author.
