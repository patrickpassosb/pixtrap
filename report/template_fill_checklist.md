# Template Fill Checklist

This file maps the draft markdown content in `report/report.md` directly to the slots inside the official Apart template (`Copy of Global South AI Safety hackathon submission template.docx`).

- [ ] **Title & Abstract**
  - Section in markdown: Frontmatter + Title + Abstract
  - Action: Copy Project Title and the Abstract text (150-250 words) into the template front page.
  - Action: Add Author Name (Patrick Passos), Affiliation, and Track (Latin America).

- [ ] **1. Introduction**
  - Section in markdown: `## 1. Introduction`
  - Action: Copy introduction text detailing the Brazilian Pix landscape and the necessity of region-specific safety. Make sure the method contribution framing is preserved.

- [ ] **2. Related Work**
  - Section in markdown: `## 2. Related Work`
  - Action: Copy citations and comparisons to existing benchmarks.

- [ ] **3. Methodology**
  - Section in markdown: `## 3. Methodology`
  - Action: Copy taxonomy descriptions, dataset sizes, model config table, and scoring criteria.
  - Action: Copy the formula for the Refusal Calibration Score.

- [ ] **4. Results**
  - Section in markdown: `## 4. Results`
  - Action: Replace placeholders with the compiled CSV tables from `results/scored/`.
  - Action: Insert `calibration_scatter.png` as the main chart.
  - Action: Insert `jailbreak_rate_by_model.png` and `over_refusal_rate_by_model.png` as supplementary figures.

- [ ] **5. Discussion**
  - Section in markdown: `## 5. Discussion`
  - Action: Copy discussion of results, regional implications, and the transferable benchmark construction recipe.

- [ ] **6. Limitations and Dual-Use Considerations**
  - Section in markdown: `## 6. Limitations and Dual-Use Considerations`
  - Action: Copy limitations.
  - Action: Copy the dual-use risk mitigation policy and gating information.
  - Action: Report the single-author delayed blind audit disagreement rate.

- [ ] **References**
  - Section in markdown: `## References`
  - Action: Verify all links work. Copy reference list into the template's references block.

- [ ] **LLM Usage Statement**
  - Section in markdown: `## LLM Usage Statement`
  - Action: Document that Antigravity was used as an interactive programming partner to implement code, run experiments, draft reports, and design charts.
