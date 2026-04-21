#!/bin/bash
# push_schedule.sh
# ─────────────────────────────────────────────────────────────────────────────
# Regenerates bootcamp day HTML pages from schedule.csv and pushes to GitHub.
#
# Workflow:
#   1. Open Google Sheet → File → Download → CSV
#   2. Rename file to: schedule.csv
#   3. Move it into this repo folder
#   4. Run: ./push_schedule.sh
#
# No OAuth, no Google Cloud, no API keys needed.
# ─────────────────────────────────────────────────────────────────────────────

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Checkr Bootcamp Schedule — Auto-Push"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── Check schedule.csv exists ─────────────────────────────────────────────────
if [ ! -f "schedule.csv" ]; then
  echo "❌  No schedule.csv found in this folder."
  echo ""
  echo "    To fix:"
  echo "    1. Open your Google Sheet"
  echo "    2. File → Download → Comma Separated Values (.csv)"
  echo "    3. Rename it to: schedule.csv"
  echo "    4. Move it here: $SCRIPT_DIR"
  echo "    5. Run this script again"
  echo ""
  exit 1
fi

# ── Step 1: Generate HTML ─────────────────────────────────────────────────────
echo "Step 1 of 3 — Generating HTML from schedule.csv..."
python3 generate_schedule.py
echo ""

# ── Step 2: Check for changes ────────────────────────────────────────────────
echo "Step 2 of 3 — Checking for changes..."

git add bootcamp_day*.html

if git diff --cached --quiet; then
  echo "  No changes detected — pages are already up to date."
  echo ""
  echo "✅  Nothing to push. Done."
  exit 0
fi

CHANGED=$(git diff --cached --name-only)
echo "  Changed files:"
echo "$CHANGED" | sed 's/^/    /'
echo ""

# ── Step 3: Commit and push ───────────────────────────────────────────────────
echo "Step 3 of 3 — Committing and pushing to GitHub..."

TIMESTAMP=$(date '+%B %d, %Y at %I:%M %p')

git commit -m "Regenerate bootcamp schedule pages — ${TIMESTAMP}

Auto-generated from schedule.csv (exported from Google Sheets)

Updated:
$(echo "$CHANGED" | sed 's/^/  - /')"

git push origin main

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅  Done! Live on GitHub Pages in ~60s:"
echo ""
echo "   Day 1: https://enablementatcheckr.github.io/Onboarding/bootcamp_day1.html"
echo "   Day 2: https://enablementatcheckr.github.io/Onboarding/bootcamp_day2.html"
echo "   Day 3: https://enablementatcheckr.github.io/Onboarding/bootcamp_day3.html"
echo "   Day 4: https://enablementatcheckr.github.io/Onboarding/bootcamp_day4.html"
echo "   Day 5: https://enablementatcheckr.github.io/Onboarding/bootcamp_day5.html"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

set -e   # exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Checkr Bootcamp Schedule — Auto-Push"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── Step 1: Generate HTML from Google Sheet ───────────────────────────────────
echo "Step 1 of 3 — Generating HTML from Google Sheet..."
python3 generate_schedule.py
echo ""

# ── Step 2: Check if there are any changes to commit ─────────────────────────
echo "Step 2 of 3 — Checking for changes..."
if git diff --quiet bootcamp_day*.html 2>/dev/null && \
   git ls-files --others --exclude-standard bootcamp_day*.html | grep -q .; then
  echo "  No changes detected — schedule is already up to date."
  echo ""
  echo "✅  Nothing to push. Done."
  exit 0
fi

CHANGED=$(git diff --name-only bootcamp_day*.html 2>/dev/null; \
          git ls-files --others --exclude-standard bootcamp_day*.html 2>/dev/null)

if [ -z "$CHANGED" ]; then
  echo "  No changes detected — schedule is already up to date."
  echo ""
  echo "✅  Nothing to push. Done."
  exit 0
fi

echo "  Changed files:"
echo "$CHANGED" | sed 's/^/    /'
echo ""

# ── Step 3: Commit and push ───────────────────────────────────────────────────
echo "Step 3 of 3 — Committing and pushing to GitHub..."

TIMESTAMP=$(date '+%B %d, %Y at %I:%M %p')

git add bootcamp_day*.html
git commit -m "Regenerate bootcamp schedule pages

Auto-generated from Google Sheet 'Bootcamp Schedule' tab
Generated: ${TIMESTAMP}

Updated files:
$(echo "$CHANGED" | sed 's/^/  - /')"

git push origin main

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅  Done! Pages are live on GitHub Pages."
echo ""
echo "   View at:"
echo "   https://enablementatcheckr.github.io/Onboarding/bootcamp_day1.html"
echo "   https://enablementatcheckr.github.io/Onboarding/bootcamp_day2.html"
echo "   https://enablementatcheckr.github.io/Onboarding/bootcamp_day3.html"
echo "   https://enablementatcheckr.github.io/Onboarding/bootcamp_day4.html"
echo "   https://enablementatcheckr.github.io/Onboarding/bootcamp_day5.html"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
