#!/usr/bin/env python3
"""
generate_schedule.py
────────────────────
Reads the "Bootcamp Schedule" CSV (exported from Google Sheets) and generates
bootcamp_day1.html … bootcamp_day5.html

Workflow:
  1. Open your Google Sheet
  2. File → Download → Comma Separated Values (.csv)
  3. Save it as 'schedule.csv' in this folder (the repo root)
  4. Run: ./push_schedule.sh  (or: python3 generate_schedule.py)

That's it. No Google Cloud, no OAuth, no tokens.
"""

import csv, os, re, sys
from datetime import datetime
from pathlib import Path

# ── CONFIGURATION ─────────────────────────────────────────────────────────────
CSV_FILE   = Path(__file__).parent / 'schedule.csv'   # drop your export here
OUTPUT_DIR = Path(__file__).parent

DAYS = {
    'Day 1': 'Monday',
    'Day 2': 'Tuesday',
    'Day 3': 'Wednesday',
    'Day 4': 'Thursday',
    'Day 5': 'Friday',
}

OUTPUT_FILES = {
    'Day 1': 'bootcamp_day1.html',
    'Day 2': 'bootcamp_day2.html',
    'Day 3': 'bootcamp_day3.html',
    'Day 4': 'bootcamp_day4.html',
    'Day 5': 'bootcamp_day5.html',
}

# ── READ CSV ──────────────────────────────────────────────────────────────────
def get_sheet_data():
    if not CSV_FILE.exists():
        print(f"""
❌  No CSV file found at:
    {CSV_FILE}

To fix this:
  1. Open your Google Sheet
  2. File → Download → Comma Separated Values (.csv)
  3. Rename the downloaded file to:  schedule.csv
  4. Move it into your repo folder:  {OUTPUT_DIR}
  5. Run this script again
""".strip())
        sys.exit(1)

    with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = [
            {k.strip(): str(v).strip() for k, v in row.items()}
            for row in reader
            if any(v.strip() for v in row.values())   # skip blank rows
        ]

    print(f"✓  Read {len(rows)} rows from {CSV_FILE.name}")
    return rows


# ── HTML HELPERS ──────────────────────────────────────────────────────────────
def format_badge(fmt):
    if not fmt:
        return ''
    key = fmt.lower().strip()
    classes = {
        'role-play':     'fb-roleplay',
        'roleplay':      'fb-roleplay',
        'workshop':      'fb-workshop',
        'presentation':  'fb-presentation',
        'certification': 'fb-cert',
        'break':         'fb-break',
        'lunch':         'fb-break',
    }
    cls = classes.get(key, 'fb-default')
    return f'<span class="fmt-badge {cls}">{fmt}</span>'


def row_class(fmt):
    return 'fmt-' + (fmt or '').lower().strip().replace(' ', '-')


def make_table_rows(rows):
    if not rows:
        return '<tr><td colspan="8" style="text-align:center;padding:40px;color:#67727C">No sessions found for this day</td></tr>'
    html = []
    for r in rows:
        fmt          = r.get('Format', '')
        presentation = r.get('Presentation', '')
        prework      = r.get('Pre-Work', '')
        notes        = r.get('Notes', '')
        presenter    = r.get('Presenter', '')
        start        = r.get('Start', '')
        duration     = r.get('Duration', '')
        session      = r.get('Session', '')
        deck_link    = (f'<a class="link-btn" href="{presentation}" target="_blank">↗ Deck</a>'
                        if presentation else '')
        html.append(f'''    <tr class="{row_class(fmt)}">
      <td class="td-time">{start}</td>
      <td class="td-dur">{duration}</td>
      <td class="td-session">{session}</td>
      <td class="td-format">{format_badge(fmt)}</td>
      <td class="td-presenter">{presenter}</td>
      <td class="td-link">{deck_link}</td>
      <td class="td-prework">{prework}</td>
      <td class="td-notes">{notes}</td>
    </tr>''')
    return '\n'.join(html)


def build_day_meta(rows):
    sessions = [r for r in rows if r.get('Format','').lower() not in ('break','lunch','')]
    formats  = list(dict.fromkeys(r.get('Format','') for r in sessions if r.get('Format')))

    total_min = 0
    for r in rows:
        d = r.get('Duration','').lower()
        hr = re.search(r'(\d+\.?\d*)\s*h', d)
        mn = re.search(r'(\d+)\s*m', d)
        if hr: total_min += float(hr.group(1)) * 60
        if mn: total_min += int(mn.group(1))

    hr_str = f"{int(total_min//60)}h {int(total_min%60)}m".strip() if total_min > 0 else ''

    chips = [f'<div class="meta-chip"><strong>{len(sessions)}</strong> sessions</div>']
    if hr_str:
        chips.append(f'<div class="meta-chip"><strong>{hr_str}</strong> total</div>')
    for f in formats:
        chips.append(f'<div class="meta-chip">{format_badge(f)}</div>')
    return '\n'.join(chips)


CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --navy: #1E448F; --teal: #45C0B9; --orange: #F37D53;
    --slate: #67727C; --bg: #F7F9FC; --border: #D4DAE1;
    --white: #fff; --dark: #0B1626;
  }
  body { font-family: 'DM Sans', sans-serif; background: var(--bg); color: var(--dark); font-size: 14px; line-height: 1.5; }
  .nav { background: var(--navy); padding: 0 28px; height: 52px; display: flex; align-items: center; position: sticky; top: 0; z-index: 100; }
  .nav .logo { color: #fff; font-weight: 600; font-size: 14px; margin-right: 28px; }
  .nav a { color: rgba(255,255,255,.65); text-decoration: none; font-size: 13px; font-weight: 500; padding: 0 14px; height: 52px; display: flex; align-items: center; border-bottom: 3px solid transparent; transition: all .15s; }
  .nav a:hover, .nav a.active { color: #fff; border-bottom-color: var(--teal); }
  .hero { background: var(--navy); padding: 28px 28px 24px; color: #fff; }
  .hero-eyebrow { font-size: 11px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: var(--teal); margin-bottom: 6px; }
  .hero h1 { font-size: 24px; font-weight: 600; margin-bottom: 4px; }
  .hero p { color: rgba(255,255,255,.6); font-size: 13px; }
  .day-tabs { background: var(--white); border-bottom: 2px solid var(--border); padding: 0 28px; display: flex; overflow-x: auto; }
  .day-tab { padding: 13px 22px; font-size: 13px; font-weight: 500; color: var(--slate); white-space: nowrap; border-bottom: 3px solid transparent; margin-bottom: -2px; text-decoration: none; display: flex; align-items: center; transition: all .15s; }
  .day-tab:hover { color: var(--navy); }
  .day-tab.active { color: var(--navy); border-bottom-color: var(--navy); font-weight: 600; }
  .main { padding: 24px 28px; max-width: 1200px; margin: 0 auto; }
  .status-bar { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--slate); margin-bottom: 16px; padding: 9px 14px; background: var(--white); border: 1px solid var(--border); border-radius: 8px; }
  .status-dot { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; flex-shrink: 0; }
  .day-meta { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; }
  .meta-chip { background: var(--white); border: 1px solid var(--border); border-radius: 7px; padding: 6px 13px; font-size: 12px; color: var(--slate); }
  .meta-chip strong { color: var(--dark); font-weight: 600; }
  .schedule-wrap { background: var(--white); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
  table { width: 100%; border-collapse: collapse; }
  thead tr { background: var(--navy); }
  thead th { padding: 11px 14px; font-size: 10.5px; font-weight: 600; letter-spacing: .09em; text-transform: uppercase; text-align: left; color: rgba(255,255,255,.85); }
  tbody tr { border-bottom: 1px solid var(--border); transition: background .1s; }
  tbody tr:last-child { border-bottom: none; }
  tbody tr:hover { background: #F4F7FD; }
  tbody tr.fmt-role-play, tbody tr.fmt-roleplay { border-left: 3px solid var(--orange); }
  tbody tr.fmt-workshop   { border-left: 3px solid var(--teal); }
  tbody tr.fmt-presentation { border-left: 3px solid var(--navy); }
  tbody tr.fmt-certification { border-left: 3px solid #8B5CF6; }
  tbody tr.fmt-break, tbody tr.fmt-lunch { border-left: 3px solid var(--border); background: #FAFBFC; }
  tbody tr.fmt-break td, tbody tr.fmt-lunch td { color: var(--slate); font-style: italic; }
  td { padding: 11px 14px; font-size: 13px; vertical-align: top; }
  .td-time { white-space: nowrap; font-weight: 600; color: var(--navy); font-size: 12px; min-width: 72px; }
  .td-dur  { color: var(--slate); font-size: 12px; white-space: nowrap; min-width: 64px; }
  .td-session { font-weight: 500; min-width: 180px; }
  .td-format { min-width: 110px; }
  .td-presenter { color: var(--slate); font-size: 12px; min-width: 100px; }
  .td-link { min-width: 80px; }
  .td-prework { font-size: 12px; color: var(--slate); min-width: 100px; }
  .td-notes { font-size: 12px; color: var(--slate); }
  .fmt-badge { display: inline-block; padding: 2px 9px; border-radius: 20px; font-size: 11px; font-weight: 600; white-space: nowrap; }
  .fb-roleplay     { background: #FEF0EB; color: #B85020; }
  .fb-workshop     { background: #E6F7F6; color: #29736F; }
  .fb-presentation { background: #EBF0FA; color: #1E448F; }
  .fb-cert         { background: #F3F0FF; color: #5B21B6; }
  .fb-break        { background: #F2F4F7; color: #67727C; }
  .fb-default      { background: #F2F4F7; color: #67727C; }
  .link-btn { display: inline-flex; align-items: center; gap: 3px; font-size: 11px; font-weight: 600; color: var(--navy); text-decoration: none; padding: 3px 8px; border: 1px solid var(--border); border-radius: 5px; transition: all .12s; }
  .link-btn:hover { background: var(--navy); color: #fff; border-color: var(--navy); }
  footer { text-align: center; padding: 28px; font-size: 12px; color: var(--slate); }
"""


def build_html(day_key, day_label, rows, generated_at):
    day_num    = day_key.split()[-1]
    table_rows = make_table_rows(rows)
    meta_chips = build_day_meta(rows)

    tab_links = []
    for dk, dl in DAYS.items():
        dn     = dk.split()[-1]
        active = ' active' if dk == day_key else ''
        tab_links.append(f'<a class="day-tab{active}" href="bootcamp_day{dn}.html">{dk} — {dl}</a>')
    tabs_html = '\n    '.join(tab_links)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bootcamp {day_key} — {day_label} · Checkr Sales Onboarding</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<nav class="nav">
  <div class="logo">Checkr Sales Onboarding</div>
  <a href="prework.html">Pre-Work</a>
  <a href="bootcamp.html" class="active">Bootcamp</a>
  <a href="milestones2.html">Milestones</a>
  <a href="playbook.html">Playbook</a>
</nav>

<div class="hero">
  <div class="hero-eyebrow">Phase 2 · Bootcamp · Week 2</div>
  <h1>Bootcamp {day_key} — {day_label}</h1>
  <p>Last updated {generated_at}</p>
</div>

<div class="day-tabs">
  {tabs_html}
</div>

<main class="main">

  <div class="status-bar">
    <div class="status-dot"></div>
    <span>{len(rows)} sessions · Generated {generated_at}</span>
  </div>

  <div class="day-meta">
    {meta_chips}
  </div>

  <div class="schedule-wrap">
    <table>
      <thead>
        <tr>
          <th>Start</th><th>Duration</th><th>Session</th><th>Format</th>
          <th>Presenter</th><th>Deck</th><th>Pre-Work</th><th>Notes</th>
        </tr>
      </thead>
      <tbody>
{table_rows}
      </tbody>
    </table>
  </div>

</main>

<footer>Checkr Sales Enablement · Bootcamp 2026 · For internal use only · Generated {generated_at}</footer>

</body>
</html>'''


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("\n🚀  Checkr Bootcamp Schedule Generator")
    print("─" * 40)

    all_rows     = get_sheet_data()
    generated_at = datetime.now().strftime('%B %d, %Y at %I:%M %p')

    if not all_rows:
        print("❌  No rows found in CSV. Is the file empty?")
        sys.exit(1)

    # Check for Day column
    headers = list(all_rows[0].keys())
    if 'Day' not in headers:
        print(f"\n⚠️   No 'Day' column found. Columns in your CSV: {', '.join(headers)}")
        print("    Add a 'Day' column to your sheet with values: Day 1, Day 2 … Day 5")
        print("    Re-export as CSV and try again.\n")
        sys.exit(1)

    # Write one file per day
    for day_key, day_label in DAYS.items():
        day_rows = [r for r in all_rows if r.get('Day','').strip() == day_key]
        html     = build_html(day_key, day_label, day_rows, generated_at)
        out_path = OUTPUT_DIR / OUTPUT_FILES[day_key]
        out_path.write_text(html, encoding='utf-8')
        print(f"  ✓  {out_path.name}  ({len(day_rows)} sessions)")

    print(f"\n✅  Done — 5 files written")
    print("    Run ./push_schedule.sh to push to GitHub\n")


if __name__ == '__main__':
    main()


import json, os, re, sys, textwrap
from datetime import datetime
from pathlib import Path

# ── CONFIGURATION ─────────────────────────────────────────────────────────────
SHEET_ID   = '1uYY0eQ-ySgun6MC7LvVc32wZHfMgchsSKtAvsUtu834'
TAB_NAME   = 'Bootcamp Schedule'
OUTPUT_DIR = Path(__file__).parent   # writes files next to this script (repo root)

DAYS = {
    'Day 1': 'Monday',
    'Day 2': 'Tuesday',
    'Day 3': 'Wednesday',
    'Day 4': 'Thursday',
    'Day 5': 'Friday',
}

OUTPUT_FILES = {
    'Day 1': 'bootcamp_day1.html',
    'Day 2': 'bootcamp_day2.html',
    'Day 3': 'bootcamp_day3.html',
    'Day 4': 'bootcamp_day4.html',
    'Day 5': 'bootcamp_day5.html',
}

TOKEN_DIR  = Path.home() / '.config' / 'checkr_bootcamp'
TOKEN_FILE = TOKEN_DIR / 'token.json'
CREDS_FILE = TOKEN_DIR / 'credentials.json'

# ── AUTH ──────────────────────────────────────────────────────────────────────
def get_sheet_data():
    """Authenticate with Google and return all rows as list of dicts."""
    try:
        import gspread
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
    except ImportError:
        print("❌  Missing packages. Run:\n    pip install gspread google-auth google-auth-oauthlib")
        sys.exit(1)

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    creds = None

    # Load cached token
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # Refresh or re-auth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDS_FILE.exists():
                print(textwrap.dedent(f"""
                ❌  No credentials.json found at:
                    {CREDS_FILE}

                To set up Google OAuth (one-time):
                1. Go to https://console.cloud.google.com/
                2. Create a project (or use an existing one)
                3. Enable the Google Sheets API
                4. Go to APIs & Services → Credentials → Create Credentials → OAuth client ID
                5. Application type: Desktop app
                6. Download the JSON → save it to:
                   {CREDS_FILE}
                7. Run this script again
                """).strip())
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Cache the token
        TOKEN_DIR.mkdir(parents=True, exist_ok=True)
        TOKEN_FILE.write_text(creds.to_json())

    client = gspread.authorize(creds)
    sheet  = client.open_by_key(SHEET_ID).worksheet(TAB_NAME)
    rows   = sheet.get_all_records()   # list of dicts, headers from row 1
    print(f"✓  Fetched {len(rows)} rows from '{TAB_NAME}'")
    return rows


# ── HTML GENERATION ───────────────────────────────────────────────────────────
def format_badge(fmt):
    if not fmt:
        return ''
    key = fmt.lower().strip()
    classes = {
        'role-play':     'fb-roleplay',
        'roleplay':      'fb-roleplay',
        'workshop':      'fb-workshop',
        'presentation':  'fb-presentation',
        'certification': 'fb-cert',
        'break':         'fb-break',
        'lunch':         'fb-break',
    }
    cls = classes.get(key, 'fb-default')
    return f'<span class="fmt-badge {cls}">{fmt}</span>'


def row_class(fmt):
    key = (fmt or '').lower().strip().replace(' ', '-')
    return f'fmt-{key}'


def make_table_rows(rows):
    if not rows:
        return '<tr><td colspan="8" style="text-align:center;padding:40px;color:#67727C">No sessions found for this day</td></tr>'
    html = []
    for r in rows:
        fmt          = str(r.get('Format', '')).strip()
        presentation = str(r.get('Presentation', '')).strip()
        prework      = str(r.get('Pre-Work', '')).strip()
        notes        = str(r.get('Notes', '')).strip()
        presenter    = str(r.get('Presenter', '')).strip()
        start        = str(r.get('Start', '')).strip()
        duration     = str(r.get('Duration', '')).strip()
        session      = str(r.get('Session', '')).strip()

        deck_link = (f'<a class="link-btn" href="{presentation}" target="_blank">↗ Deck</a>'
                     if presentation else '')

        html.append(f'''    <tr class="{row_class(fmt)}">
      <td class="td-time">{start}</td>
      <td class="td-dur">{duration}</td>
      <td class="td-session">{session}</td>
      <td class="td-format">{format_badge(fmt)}</td>
      <td class="td-presenter">{presenter}</td>
      <td class="td-link">{deck_link}</td>
      <td class="td-prework">{prework}</td>
      <td class="td-notes">{notes}</td>
    </tr>''')
    return '\n'.join(html)


def build_day_meta(rows):
    """Build summary chip HTML for a day."""
    sessions = [r for r in rows if (r.get('Format') or '').lower() not in ('break','lunch','')]
    formats  = list(dict.fromkeys(
        str(r.get('Format','')).strip() for r in sessions if r.get('Format')
    ))

    # Parse total duration
    total_min = 0
    for r in rows:
        d = str(r.get('Duration','')).lower()
        hr  = re.search(r'(\d+\.?\d*)\s*h', d)
        mn  = re.search(r'(\d+)\s*m', d)
        if hr:  total_min += float(hr.group(1)) * 60
        if mn:  total_min += int(mn.group(1))

    hr_str = (f"{int(total_min//60)}h {int(total_min%60)}m".strip()
              if total_min > 0 else '')

    chips = [f'<div class="meta-chip"><strong>{len(sessions)}</strong> sessions</div>']
    if hr_str:
        chips.append(f'<div class="meta-chip"><strong>{hr_str}</strong> total</div>')
    for f in formats:
        chips.append(f'<div class="meta-chip">{format_badge(f)}</div>')
    return '\n'.join(chips)


CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --navy: #1E448F; --teal: #45C0B9; --orange: #F37D53;
    --slate: #67727C; --bg: #F7F9FC; --border: #D4DAE1;
    --white: #fff; --dark: #0B1626;
  }
  body { font-family: 'DM Sans', sans-serif; background: var(--bg); color: var(--dark); font-size: 14px; line-height: 1.5; }

  /* NAV */
  .nav { background: var(--navy); padding: 0 28px; height: 52px; display: flex; align-items: center; position: sticky; top: 0; z-index: 100; }
  .nav .logo { color: #fff; font-weight: 600; font-size: 14px; margin-right: 28px; }
  .nav a { color: rgba(255,255,255,.65); text-decoration: none; font-size: 13px; font-weight: 500; padding: 0 14px; height: 52px; display: flex; align-items: center; border-bottom: 3px solid transparent; transition: all .15s; }
  .nav a:hover, .nav a.active { color: #fff; border-bottom-color: var(--teal); }

  /* HERO */
  .hero { background: var(--navy); padding: 28px 28px 24px; color: #fff; }
  .hero-eyebrow { font-size: 11px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: var(--teal); margin-bottom: 6px; }
  .hero h1 { font-size: 24px; font-weight: 600; margin-bottom: 4px; }
  .hero p { color: rgba(255,255,255,.6); font-size: 13px; }

  /* DAY TABS */
  .day-tabs { background: var(--white); border-bottom: 2px solid var(--border); padding: 0 28px; display: flex; overflow-x: auto; }
  .day-tab { padding: 13px 22px; font-size: 13px; font-weight: 500; color: var(--slate); white-space: nowrap; border-bottom: 3px solid transparent; margin-bottom: -2px; text-decoration: none; display: flex; align-items: center; transition: all .15s; }
  .day-tab:hover { color: var(--navy); }
  .day-tab.active { color: var(--navy); border-bottom-color: var(--navy); font-weight: 600; }

  /* MAIN */
  .main { padding: 24px 28px; max-width: 1200px; margin: 0 auto; }

  /* STATUS */
  .status-bar { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--slate); margin-bottom: 16px; padding: 9px 14px; background: var(--white); border: 1px solid var(--border); border-radius: 8px; }
  .status-dot { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; flex-shrink: 0; }

  /* META CHIPS */
  .day-meta { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; }
  .meta-chip { background: var(--white); border: 1px solid var(--border); border-radius: 7px; padding: 6px 13px; font-size: 12px; color: var(--slate); }
  .meta-chip strong { color: var(--dark); font-weight: 600; }

  /* TABLE */
  .schedule-wrap { background: var(--white); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
  table { width: 100%; border-collapse: collapse; }
  thead tr { background: var(--navy); }
  thead th { padding: 11px 14px; font-size: 10.5px; font-weight: 600; letter-spacing: .09em; text-transform: uppercase; text-align: left; color: rgba(255,255,255,.85); }
  tbody tr { border-bottom: 1px solid var(--border); transition: background .1s; }
  tbody tr:last-child { border-bottom: none; }
  tbody tr:hover { background: #F4F7FD; }
  tbody tr.fmt-role-play  { border-left: 3px solid var(--orange); }
  tbody tr.fmt-roleplay   { border-left: 3px solid var(--orange); }
  tbody tr.fmt-workshop   { border-left: 3px solid var(--teal); }
  tbody tr.fmt-presentation { border-left: 3px solid var(--navy); }
  tbody tr.fmt-certification { border-left: 3px solid #8B5CF6; }
  tbody tr.fmt-break, tbody tr.fmt-lunch { border-left: 3px solid var(--border); background: #FAFBFC; }
  tbody tr.fmt-break td, tbody tr.fmt-lunch td { color: var(--slate); font-style: italic; }
  td { padding: 11px 14px; font-size: 13px; vertical-align: top; }
  .td-time { white-space: nowrap; font-weight: 600; color: var(--navy); font-size: 12px; min-width: 72px; }
  .td-dur  { color: var(--slate); font-size: 12px; white-space: nowrap; min-width: 64px; }
  .td-session { font-weight: 500; min-width: 180px; }
  .td-format { min-width: 110px; }
  .td-presenter { color: var(--slate); font-size: 12px; min-width: 100px; }
  .td-link { min-width: 80px; }
  .td-prework { font-size: 12px; color: var(--slate); min-width: 100px; }
  .td-notes { font-size: 12px; color: var(--slate); }

  /* BADGES */
  .fmt-badge { display: inline-block; padding: 2px 9px; border-radius: 20px; font-size: 11px; font-weight: 600; white-space: nowrap; }
  .fb-roleplay     { background: #FEF0EB; color: #B85020; }
  .fb-workshop     { background: #E6F7F6; color: #29736F; }
  .fb-presentation { background: #EBF0FA; color: #1E448F; }
  .fb-cert         { background: #F3F0FF; color: #5B21B6; }
  .fb-break        { background: #F2F4F7; color: #67727C; }
  .fb-default      { background: #F2F4F7; color: #67727C; }
  .link-btn { display: inline-flex; align-items: center; gap: 3px; font-size: 11px; font-weight: 600; color: var(--navy); text-decoration: none; padding: 3px 8px; border: 1px solid var(--border); border-radius: 5px; transition: all .12s; }
  .link-btn:hover { background: var(--navy); color: #fff; border-color: var(--navy); }

  /* FOOTER */
  footer { text-align: center; padding: 28px; font-size: 12px; color: var(--slate); }
"""


def build_html(day_key, day_label, rows, generated_at):
    day_num   = day_key.split()[-1]   # '1', '2' etc
    table_rows = make_table_rows(rows)
    meta_chips = build_day_meta(rows)

    # Build tab links
    tab_links = []
    for dk, dl in DAYS.items():
        dn     = dk.split()[-1]
        active = ' active' if dk == day_key else ''
        tab_links.append(
            f'<a class="day-tab{active}" href="bootcamp_day{dn}.html">{dk} — {dl}</a>'
        )
    tabs_html = '\n    '.join(tab_links)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bootcamp {day_key} — {day_label} · Checkr Sales Onboarding</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<nav class="nav">
  <div class="logo">Checkr Sales Onboarding</div>
  <a href="prework.html">Pre-Work</a>
  <a href="bootcamp.html" class="active">Bootcamp</a>
  <a href="milestones2.html">Milestones</a>
  <a href="playbook.html">Playbook</a>
</nav>

<div class="hero">
  <div class="hero-eyebrow">Phase 2 · Bootcamp · Week 2</div>
  <h1>Bootcamp {day_key} — {day_label}</h1>
  <p>Generated {generated_at} · Edit your Google Sheet and run <code>generate_schedule.py</code> to refresh</p>
</div>

<div class="day-tabs">
  {tabs_html}
</div>

<main class="main">

  <div class="status-bar">
    <div class="status-dot"></div>
    <span>Static page · {len(rows)} sessions · Last generated {generated_at}</span>
  </div>

  <div class="day-meta">
    {meta_chips}
  </div>

  <div class="schedule-wrap">
    <table>
      <thead>
        <tr>
          <th>Start</th><th>Duration</th><th>Session</th><th>Format</th>
          <th>Presenter</th><th>Deck</th><th>Pre-Work</th><th>Notes</th>
        </tr>
      </thead>
      <tbody>
{table_rows}
      </tbody>
    </table>
  </div>

</main>

<footer>Checkr Sales Enablement · Bootcamp 2026 · For internal use only · Generated {generated_at}</footer>

</body>
</html>'''


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("\n🚀  Checkr Bootcamp Schedule Generator")
    print("─" * 40)

    all_rows    = get_sheet_data()
    generated_at = datetime.now().strftime('%B %d, %Y at %I:%M %p')

    # Check for Day column
    if all_rows and 'Day' not in all_rows[0]:
        print("\n⚠️   No 'Day' column found in your sheet.")
        print("    Add a column called 'Day' with values Day 1, Day 2 … Day 5")
        print("    to each row, then run this script again.\n")
        print("    Writing a single combined page instead: bootcamp_schedule_all.html")
        # Write all rows to a single file as fallback
        rows_html = make_table_rows(all_rows)
        html = build_html('Day 1', 'All Days', all_rows, generated_at)
        out  = OUTPUT_DIR / 'bootcamp_schedule_all.html'
        out.write_text(html, encoding='utf-8')
        print(f"    ✓  Written: {out}")
        return

    # Split by day and write one file per day
    files_written = []
    for day_key, day_label in DAYS.items():
        day_rows = [r for r in all_rows if str(r.get('Day','')).strip() == day_key]
        html     = build_html(day_key, day_label, day_rows, generated_at)
        out_path = OUTPUT_DIR / OUTPUT_FILES[day_key]
        out_path.write_text(html, encoding='utf-8')
        files_written.append(out_path.name)
        print(f"  ✓  {out_path.name}  ({len(day_rows)} sessions)")

    print(f"\n✅  Done — {len(files_written)} files written to {OUTPUT_DIR}")
    print("\nNext step: run push_schedule.sh to commit and push to GitHub\n")


if __name__ == '__main__':
    main()
