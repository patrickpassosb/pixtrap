#!/bin/bash
# Build PixTrap report PDF from Markdown
# Usage: ./scripts/build_report.sh

set -e

echo "Building PixTrap report PDF..."

# Activate venv
source "$(dirname "$0")/../.venv/bin/activate"

# Install weasyprint if not present
if ! python -c "import weasyprint" 2>/dev/null; then
    echo "Installing weasyprint..."
    uv pip install weasyprint
fi

# Markdown -> HTML -> PDF
echo "Converting Markdown to HTML..."
pandoc report/report.md \
    -f markdown \
    -t html5 \
    --standalone \
    --embed-resources \
    --css=report/style.css \
    --metadata pagetitle="PixTrap Report" \
    -o report/report.html

echo "Converting HTML to PDF..."
python -c "from weasyprint import HTML; HTML('report/report.html').write_pdf('submission/final_report/pixtrap_report.pdf')"

echo "Done! PDF saved to: submission/final_report/pixtrap_report.pdf"
