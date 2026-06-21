# PixTrap Walkthrough Video Script (2-3 Minutes)

## [0:00 - 0:15] Problem & Thesis
- **Visual**: Title slide with "PixTrap: Do Models Know When Pix Help Becomes Pix Fraud?". Show a map of Brazil.
- **Audio**: "Hello, my name is Patrick, and today I'm presenting PixTrap, a Brazilian Portuguese safety benchmark. Language model safety evaluations are predominantly English-centric. However, local deployments face highly specific regional risks. In Brazil, the instant payment system, Pix, is used by over 150 million people, making it the primary target for social engineering, WhatsApp cloning, and payment fraud."

## [0:15 - 0:45] Taxonomy & Near-Neighbors
- **Visual**: Slide showing the taxonomy: Impersonation, Urgency Coercion, Fake Receipts, Recovery Scams.
- **Audio**: "PixTrap evaluates models across these four critical Brazil-specific fraud categories. To make this a rigorous safety benchmark rather than a simple refusal test, we introduce a near-neighbor calibration design. We pair every harmful prompt—like asking to generate a fake receipt—with a benign, legitimate near-neighbor—like a vendor asking how to protect themselves from fake receipts. This allows us to measure whether models can refuse the fraud while still helping the victim."

## [0:45 - 1:15] Model Roster & Methodology
- **Visual**: Slide showing the 5 models evaluated and the evaluation flow: prompts -> API calls -> automatic scoring -> manual review.
- **Audio**: "We evaluated five diverse models—including GLM 5.2, DeepSeek V4 Flash, Llama 3.3, Gemma 4, and MiniMax M3. Each model was evaluated on both pt-BR prompts and matched English baselines. To ensure high-quality labels, we used a multi-label classification rubric and performed a delayed blind manual audit on a subset of responses to validate our automated heuristics."

## [1:15 - 2:00] Results & Key Chart
- **Visual**: The calibration scatter plot. Point out the "Ideal Zone" (lower-left), show how models change from English (faded) to pt-BR (solid).
- **Audio**: "Here is our main result. On the X-axis, we have the harmful compliance rate, and on the Y-axis, we have the over-refusal rate. The lower-left corner is the ideal safe zone. Notice the gap connected by the dotted lines: when shifted from English to Portuguese, models frequently experience safety regression—either becoming more compliant with fraud or over-refusing legitimate help requests due to keyword triggers. For example, Llama 3.3 shows high safety in English but exhibits over-refusal and compliance gaps in Portuguese."

## [2:00 - 2:30] Implications & Gating Policy
- **Visual**: GitHub repository screen or taxonomy diagram. Public release policy slide.
- **Audio**: "These results demonstrate that cultural and linguistic context matters deeply for AI safety. PixTrap is designed to be low-cost, reproducible, and easy to resume. Because these prompts represent real-world social-engineering risks, we gate the raw harmful dataset to prevent misuse, while publishing the code, scoring heuristics, and sanitized samples. We hope this methodology serves as a reusable template for other local AI safety benchmarks worldwide. Thank you."
