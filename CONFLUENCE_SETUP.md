# Hosting the Bootcamp Schedule on Confluence

A guide for moving the Checkr Sales Onboarding schedule pages from GitHub Pages
to Confluence — behind Checkr's firewall, with native Google Sheets integration.

---

## Why Confluence works better here

| | GitHub Pages | Confluence |
|---|---|---|
| Behind firewall | ❌ | ✅ |
| Google auth built in | ❌ | ✅ |
| Live Google Sheets embed | ❌ (CORS blocked) | ✅ |
| IT approved | ⚠️ Under review | ✅ |
| Edit without code | ❌ | ✅ |

---

## Option A — Embed your Google Sheet directly (recommended)

This is the simplest path. Confluence has a native Google Sheets macro
that embeds your sheet live inside any page.

### Steps

1. **Open Confluence** and navigate to your Sales Enablement space
2. **Create a new page** (or edit an existing one)
3. Click the **+** Insert button → search for **Google Sheets**
4. Paste your sheet URL:
   `https://docs.google.com/spreadsheets/d/1uYY0eQ-ySgun6MC7LvVc32wZHfMgchsSKtAvsUtu834`
5. The sheet embeds live — anyone on Checkr's network sees real-time data
6. **No Day column needed** — you can show the full sheet or specific ranges

### Showing a specific range (e.g. Day 1 only)

In the Google Sheets macro settings, set the **Range** field to:
`'Bootcamp Schedule'!A1:I50`

Adjust the row range per day. Or use one Confluence page per day,
each embedding a named range.

### Tip: Named ranges make this much cleaner

In your Google Sheet:
- Select Day 1 rows → **Data → Named ranges** → name it `Day1`
- Repeat for Day 2–5
- In each Confluence page, embed range `Day1`, `Day2`, etc.
- When you add/remove rows in the sheet, the named range updates automatically

---

## Option B — Paste the generated HTML using the HTML macro

Use this if you want the styled, branded version (with the navy header,
format badges, and Checkr design system) rather than a raw sheet embed.

### Steps

1. Run `generate_schedule.py` locally to produce `bootcamp_day1.html` … `bootcamp_day5.html`
2. In Confluence, create a new page
3. Click **Insert → Other macros** → search for **HTML**
   *(Note: the HTML macro may need to be enabled by your Confluence admin)*
4. Open `bootcamp_day1.html` in a text editor
5. Copy everything **between** `<body>` and `</body>` (not the full file)
6. Paste into the HTML macro
7. Save the page

### Limitation

The HTML macro strips `<style>` tags in some Confluence configurations.
If styles disappear, use **Option C** instead.

---

## Option C — Confluence page with manual table (no code needed)

If neither macro is available, the fastest path is a native Confluence table
that you update manually — but link it to the sheet so it's clear where
the source of truth lives.

### Steps

1. Create a Confluence page called **Bootcamp Schedule — Day 1**
2. Add a callout at the top:
   > 📋 Source of truth: [Bootcamp Schedule Google Sheet](https://docs.google.com/spreadsheets/d/1uYY0eQ-ySgun6MC7LvVc32wZHfMgchsSKtAvsUtu834)
3. Insert a table with columns: **Start / Duration / Session / Format / Presenter / Deck / Pre-Work / Notes**
4. Paste your Day 1 rows
5. Repeat for Days 2–5

This requires manual sync when the sheet changes, but is zero-dependency
and works in any Confluence instance.

---

## Recommended page structure in Confluence

```
Sales Enablement (Space)
└── New Hire Onboarding (Page)
    ├── Bootcamp Overview
    ├── Bootcamp Day 1 — Monday
    ├── Bootcamp Day 2 — Tuesday
    ├── Bootcamp Day 3 — Wednesday
    ├── Bootcamp Day 4 — Thursday
    └── Bootcamp Day 5 — Friday
```

Use Confluence's **Table of Contents** macro on the Overview page to
auto-link to all five day pages.

---

## Asking IT to enable the HTML macro

If you go with Option B and the HTML macro isn't available, send IT this request:

> Hi — I'm building the Sales Onboarding program and need the Confluence HTML macro
> enabled for the Sales Enablement space. This would allow me to embed branded
> training schedule pages without needing external hosting. The content is
> internal-only (no external scripts or iframes). Space: Sales Enablement.
> Can you enable `html` macro for that space?

Most Confluence admins can enable this per-space in under 5 minutes.

---

## Questions?

Reach out to Nicole (Sales Enablement) or open a ticket with IT.
