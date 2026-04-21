#!/bin/bash
# push_schedule.sh
# ─────────────────────────────────────────────────────────────────────────────
# Regenerates the bootcamp day HTML pages from Google Sheets and pushes
# them to GitHub in one command.
#
# Usage:
#   ./push_schedule.sh
#
# First-time setup:
#   chmod +x push_schedule.sh
# ─────────────────────────────────────────────────────────────────────────────

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
