#!/usr/bin/env bash
# Build PixTrap report PDF from LaTeX source via tectonic (XeLaTeX).
# Usage: bash scripts/build_report_latex.sh

set -euo pipefail

REPORT_DIR="report"
OUTPUT_DIR="submission/final_report"
TEX_FILE="${REPORT_DIR}/pixtrap_report.tex"
OUTPUT_PDF="${OUTPUT_DIR}/pixtrap_report.pdf"

echo "Building PixTrap report PDF with tectonic..."

# Locate tectonic
TECTONIC="${TECTONIC:-$(command -v tectonic || echo "$HOME/.local/bin/tectonic")}"
if ! command -v "${TECTONIC}" &> /dev/null && [ ! -x "${TECTONIC}" ]; then
    echo "Error: tectonic not found. Install with:" >&2
    echo "  curl -sSL -o /tmp/tectonic.tar.gz https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.16.9/tectonic-0.16.9-x86_64-unknown-linux-musl.tar.gz" >&2
    echo "  tar xzf /tmp/tectonic.tar.gz -C ~/.local/bin && chmod +x ~/.local/bin/tectonic" >&2
    exit 1
fi

mkdir -p "${OUTPUT_DIR}"

# tectonic runs XeLaTeX + biber automatically, caching packages under ~/.cache/Tectonic.
"${TECTONIC}" "${TEX_FILE}" --outdir "${OUTPUT_DIR}" --keep-logs

# tectonic names output after the .tex basename; rename to expected path.
if [ -f "${OUTPUT_DIR}/pixtrap_report.pdf" ]; then
    echo "Done! PDF saved to: ${OUTPUT_PDF}"
else
    echo "Error: expected output ${OUTPUT_PDF} not found." >&2
    ls -la "${OUTPUT_DIR}" >&2
    exit 1
fi
