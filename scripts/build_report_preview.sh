#!/usr/bin/env bash
# build_report_preview.sh
#
# IMPORTANT: This script is a best-effort helper for exporting a draft
# preview PDF from the Markdown report. The OFFICIAL submission artifact
# is the PDF exported from the Apart DOCX template, NOT this preview.
#
# Prerequisites: pandoc installed (apt install pandoc)
#
# Usage:
#   bash scripts/build_report_preview.sh

set -euo pipefail

REPORT_DIR="report"
OUTPUT_DIR="report"

echo "=== PixTrap Report Preview Builder ==="
echo ""
echo "NOTE: This generates a DRAFT preview only."
echo "The official submission PDF must be exported from the Apart DOCX template."
echo ""

if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc is not installed. Install with: sudo apt install pandoc"
    echo "Alternatively, use 'quarto render' if quarto is available."
    exit 1
fi

echo "Building DOCX preview from report/report.md ..."
pandoc "${REPORT_DIR}/report.md" \
    -o "${OUTPUT_DIR}/report_preview.docx" \
    --from markdown \
    --to docx \
    --standalone

echo "Building PDF preview from report/report.md ..."
pandoc "${REPORT_DIR}/report.md" \
    -o "${OUTPUT_DIR}/report_preview.pdf" \
    --from markdown \
    --to pdf \
    --pdf-engine=xelatex \
    2>/dev/null || {
        echo "PDF generation failed (xelatex may not be installed)."
        echo "DOCX preview was generated successfully: ${OUTPUT_DIR}/report_preview.docx"
        echo "You can convert the DOCX to PDF manually."
    }

echo ""
echo "Done. Preview files:"
ls -la "${OUTPUT_DIR}/report_preview"* 2>/dev/null || true
echo ""
echo "REMINDER: The final submission PDF must be exported from the official"
echo "Apart DOCX template, NOT from this preview."
