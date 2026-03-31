# Checkr Sales Bootcamp 2026 — Feedback Forms Setup Guide

## What you have

5 HTML feedback forms (one per bootcamp day) that collect:
- Attendee email, role, and session date
- 1–5 star rating for every session that day (matrix layout)
- 3 open-text questions

Responses are sent to a Google Sheet via a Google Apps Script Web App.

---

## Step 1 — Create the Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com) and create a new blank spreadsheet
2. Name it **Checkr Bootcamp 2026 Feedback**
3. Copy the Sheet ID from the URL — it's the long string between `/d/` and `/edit`:
   `https://docs.google.com/spreadsheets/d/`**THIS_IS_THE_SHEET_ID**`/edit`

---

## Step 2 — Set up the Google Apps Script

1. In your Google Sheet, click **Extensions → Apps Script**
2. Delete the default `myFunction()` code
3. Paste the entire contents of `google_apps_script.js`
4. Replace `YOUR_GOOGLE_SHEET_ID_HERE` with your actual Sheet ID from Step 1
5. Click **Save** (💾), name the project **Bootcamp Feedback Receiver**
6. Click **Deploy → New deployment**
   - Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
7. Click **Deploy** → authorize the permissions when prompted
8. Copy the **Web App URL** — it looks like:
   `https://script.google.com/macros/s/XXXXXXXXXX/exec`

---

## Step 3 — Connect the forms

In each of the 5 HTML files, find this line near the bottom:

```js
var SCRIPT_URL = 'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE';
```

Replace `YOUR_GOOGLE_APPS_SCRIPT_URL_HERE` with the Web App URL from Step 2.
Do this in all 5 files.

---

## Step 4 — Host the forms

Upload the 5 HTML files to your GitHub Pages repo alongside the other onboarding pages.
The URLs will be:
- `https://yourusername.github.io/repo/bootcamp_day1_feedback.html`
- `https://yourusername.github.io/repo/bootcamp_day2_feedback.html`
- ...and so on

Share the link for the relevant day at the end of each bootcamp session.

---

## Where responses go

Each day's responses land in a separate tab in your Google Sheet:
- **Day 1** tab — Monday responses
- **Day 2** tab — Tuesday responses
- etc.

Each tab has a header row (navy background) with: Timestamp, Email, Role,
Session Date, one column per session rating, then the 3 open-text fields.
