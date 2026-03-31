// ═══════════════════════════════════════════════════════════════════════════
// Checkr Sales Bootcamp 2026 — Feedback Form Receiver v3
// Submit method: HTML form POST to Web App (no fetch, no CORS)
// Deploy: Web App | Execute as: Me | Access: Anyone
// ═══════════════════════════════════════════════════════════════════════════

var SHEET_ID = 'YOUR_GOOGLE_SHEET_ID_HERE';

function doPost(e) {
  try {
    var p     = e.parameter;
    var day   = parseInt(p.day);
    var ss    = SpreadsheetApp.openById(SHEET_ID);
    var tab   = 'Day ' + day;
    var sheet = ss.getSheetByName(tab) || ss.insertSheet(tab);

    // Collect session names from hidden inputs (sn_0, sn_1, ...)
    var sessions = [];
    var i = 0;
    while (p['sn_' + i] !== undefined) {
      sessions.push(p['sn_' + i]);
      i++;
    }

    // Write header row on first use
    if (sheet.getLastRow() === 0) {
      var headers = ['Timestamp', 'Email', 'Role', 'Session Date'];
      sessions.forEach(function(s) { headers.push(s + ' (1-5)'); });
      headers.push('Most Valuable', 'Could Improve', 'Additional Notes');
      sheet.appendRow(headers);
      var hr = sheet.getRange(1, 1, 1, headers.length);
      hr.setBackground('#1E448F');
      hr.setFontColor('#FFFFFF');
      hr.setFontWeight('bold');
      sheet.setFrozenRows(1);
      // Auto-size columns
      sheet.autoResizeColumns(1, headers.length);
    }

    // Build data row
    var row = [
      new Date(),
      p.email  || '',
      p.role   || '',
      p.sdate  || ''
    ];
    for (var j = 0; j < sessions.length; j++) {
      row.push(p['r_' + j] || '');
    }
    row.push(p.highlight || '', p.improve || '', p.other || '');
    sheet.appendRow(row);

    // Return a plain success page (shown briefly in hidden iframe — user never sees it)
    return HtmlService.createHtmlOutput('<p>OK</p>');

  } catch(err) {
    return HtmlService.createHtmlOutput('<p>Error: ' + err.toString() + '</p>');
  }
}

// Visit Web App URL directly to test connectivity
function doGet(e) {
  // Add ?test=1 to the URL to write a test row and verify sheet access
  if (e && e.parameter && e.parameter.test === '1') {
    try {
      var ss    = SpreadsheetApp.openById(SHEET_ID);
      var sheet = ss.getSheetByName('Test') || ss.insertSheet('Test');
      sheet.appendRow([new Date(), 'TEST — delete me']);
      return HtmlService.createHtmlOutput('<h2>✅ Sheet access confirmed!</h2><p>Check your Google Sheet for a Test tab. Delete that row when done.</p>');
    } catch(err) {
      return HtmlService.createHtmlOutput('<h2>❌ Failed</h2><p>' + err.toString() + '</p><p>Check that SHEET_ID is correct and the script has permission to access it.</p>');
    }
  }
  return HtmlService.createHtmlOutput('<h2>✅ Receiver is live</h2><p>Checkr Bootcamp Feedback · v3</p>');
}
