================================================================================
 👥 TEAM ONBOARDING GUIDE - PBI SCOPING TOOL
================================================================================

Welcome! Your team can now use the Power BI Field Router tool to efficiently
scope field changes during Power BI migrations.

Created by: Manish Kumar Yadav
Repository: https://github.com/provanamanish/pbi-scoping-tool

================================================================================
 🎯 WHAT IS THIS TOOL?
================================================================================

The Power BI Field Router automatically maps fields from your OLD Power BI
report to your NEW Power BI report during upgrades or migrations.

Why it's useful:
  ✅ Saves hours of manual field mapping
  ✅ Identifies missing fields automatically
  ✅ Rates confidence of each match (exact, likely, possible, weak)
  ✅ Exports results as CSV or Excel
  ✅ No need to install anything locally - access via web browser

Perfect for:
  • Power BI report upgrades
  • Data model migrations
  • Field naming standardization
  • Documentation of field mappings

================================================================================
 🌐 HOW TO ACCESS
================================================================================

Your team can access the tool using ANY of these URLs:

OPTION 1: LOCAL NETWORK (if Manish's computer is on)
────────────────────────────────────────────────────────────────────────────
  http://IDAP-VM2:5000/
  or
  http://172.20.240.102:5000/

  Works on: Same WiFi/network as Manish's computer
  Starts: When Manish runs: python3.14 app.py
  Speed: Fast (local network)

OPTION 2: NGROK (Instant public access - 5 min setup)
────────────────────────────────────────────────────────────────────────────
  https://xxxx-xxxx-xxx.ngrok.io/
  
  Works on: Anywhere (internet access needed)
  Setup time: 5 minutes
  Available: As long as Manish's laptop is on
  URL changes: Every restart (or pay for custom domain)
  
  Status: Coming soon! Manish will share link in team chat

OPTION 3: PERMANENT HOSTING (Coming week 2)
────────────────────────────────────────────────────────────────────────────
  https://pbi-scoping-tool.company.com/
  (or similar - exact URL TBD)
  
  Works on: Anywhere, anytime (24/7)
  Setup time: 15-30 minutes
  Reliability: Professional hosting provider
  Cost: Free or minimal (depending on provider)

================================================================================
 📋 QUICK START (5 MINUTES)
================================================================================

1. OPEN THE TOOL
   Copy-paste the URL from team chat into your browser

2. UPLOAD YOUR REPORTS
   ✅ Upload your OLD Power BI report (.pbix file)
   ✅ Upload your NEW Power BI report (.pbix file)
   → Click "Analyze reports"

3. SELECT A PAGE
   Choose which page from the OLD report you want to map
   You'll see a preview: field count, hidden status, page type

4. VIEW FIELD MAPPINGS
   See a color-coded table:
   🟢 Green  = Exact matches (100% confidence)
   🟡 Yellow = Likely/possible matches (need review)
   🔴 Red    = No match found (needs manual creation)

5. DOWNLOAD RESULTS
   Export as CSV or Excel with:
   • Field names
   • Match status
   • Confidence scores
   • Notes for manual review

================================================================================
 ❓ FREQUENTLY ASKED QUESTIONS
================================================================================

Q: Do my .pbix files get uploaded to the internet?
A: No! Files stay on YOUR machine (local network or Manish's computer).
   Nothing leaves your network or is stored permanently.

Q: What Power BI versions does it support?
A: Works with both old (.pbix files from 2020+) and new format files.
   Automatically detects format.

Q: Can I use it offline?
A: For option 1 (network access): Yes, doesn't need internet
   For option 2 (ngrok): No, needs internet connection
   For option 3 (permanent hosting): No, needs internet

Q: What if the field doesn't match?
A: The tool shows "No match found". You'll need to:
   1. Review the field name in both reports
   2. Create the field in the new report if it's missing
   3. Update DAX expressions if they exist

Q: Can I use this for multiple reports?
A: Yes! Just upload different .pbix files. One tool, unlimited reports.

Q: What happens to my data?
A: Temporary files stored in Windows temp folder while you're using the tool.
   Deleted automatically when session ends.
   No data stored on any server.

Q: Is this secure?
A: Yes! 
   ✅ No credentials needed
   ✅ No sign-in required
   ✅ Local processing only
   ✅ HTTPS when deployed publicly
   ✅ Source code audited and verified

Q: Can I access this from home?
A: Option 1 (network): No, only on company network
   Option 2 (ngrok): Yes, from anywhere
   Option 3 (hosting): Yes, from anywhere
   Contact Manish to see which option is active

Q: The tool seems slow?
A: First load analyzes both reports (takes 30-60 sec)
   This is normal - large reports take longer
   Subsequent operations are instant

================================================================================
 🎓 TUTORIAL - STEP BY STEP
================================================================================

SCENARIO: You're migrating Sales Report from v1 to v2

Step 1: Prepare your files
────────────────────────────────────────────────────────────────────────────
  Find on your computer:
    ✅ SalesReport_v1.pbix   (old version)
    ✅ SalesReport_v2.pbix   (new version)

Step 2: Open the tool
────────────────────────────────────────────────────────────────────────────
  Open browser → Paste URL from team chat

Step 3: Upload old report
────────────────────────────────────────────────────────────────────────────
  Click box labeled "OLD REPORT"
  → Select: SalesReport_v1.pbix
  → File appears in the box

Step 4: Upload new report
────────────────────────────────────────────────────────────────────────────
  Click box labeled "NEW REPORT"
  → Select: SalesReport_v2.pbix
  → File appears in the box

Step 5: Click "Analyze reports"
────────────────────────────────────────────────────────────────────────────
  Wait 30-60 seconds while tool:
  • Reads both report structures
  • Extracts all fields
  • Builds comparison index
  • Shows result: "Pages found: 5" or similar

Step 6: Select a page
────────────────────────────────────────────────────────────────────────────
  Dropdown appears with page names:
    [ ] Sales by Region
    [ ] Monthly Trends
    [ ] Executive Summary
    [✓] Summary (currently selected)
  
  Right panel shows:
    📄 Summary
    📊 42 fields detected
    🎯 Power BI report page

Step 7: Review field mappings
────────────────────────────────────────────────────────────────────────────
  Table shows each field from OLD report:
  
  Old Field → Status → New Field
  OrderID   → Exact match (100%) → OrderID
  SalesAmt  → Likely match (94%) → SalesAmount
  Region    → No match → (create manually)

Step 8: Download results
────────────────────────────────────────────────────────────────────────────
  Click "Download Excel" or "Download CSV"
  → File saves to your Downloads folder
  → Open in Excel, review matches
  → Use for documentation or further processing

Done! ✅

================================================================================
 ✨ COLOR MEANINGS
================================================================================

In the results table:

🟢 GREEN (Exact match - 100%)
   Old field and new field are identical
   Safe to map without review

🟡 YELLOW (Likely/Possible - 60-99%)
   Field names are similar but not exact
   Review and confirm before using

🔴 RED (No match - 0%)
   Field doesn't exist in new report
   You'll need to recreate it

⚠️  MISSING (Yellow warning badge)
   Field exists in old report but is missing entirely from new report
   Priority: Create this field or investigate why it's gone

================================================================================
 📊 EXPORT FORMAT
================================================================================

When you download CSV/Excel, you get:

Column headers:
  • Old Table      (table name in old report)
  • Old Field      (field name in old report)
  • Type           (Column, Measure, Hierarchy Level)
  • Match Status   (Exact/Likely/Possible/No match)
  • New Table      (matching table in new report, if any)
  • New Field      (matching field in new report, if any)
  • Confidence %   (0-100% how sure the match is)
  • DAX / Expression (formula, if available)
  • Notes          (human-readable guidance)

Use this file for:
  ✅ Documentation
  ✅ Mapping configuration
  ✅ Migration checklist
  ✅ Team review process

================================================================================
 🆘 HELP & TROUBLESHOOTING
================================================================================

"Tool won't load"
  → Check URL is correct (ask Manish for current URL)
  → If option 1: Verify Manish's computer is on and connected
  → If option 2: Check internet connection
  → Try refreshing browser (Ctrl+F5)

"Files won't upload"
  → Make sure files are .pbix (not .xlsx or other type)
  → File size under 500 MB (recommended)
  → Try different browser (Chrome, Edge, Firefox)

"No fields showing in results"
  → Page might be empty (contains no visuals)
  → Try selecting a different page
  → Verify files are valid Power BI reports

"Match confidence seems low"
  → Naming styles differ (camelCase vs snake_case)
  → Field was renamed in new report
  → Field structure changed significantly
  → Manual review recommended

"Can't download CSV/Excel"
  → Try again - sometimes browser cache is issue
  → Use different browser
  → Contact Manish if problem persists

Still stuck? Ask Manish or check README.md in the GitHub repo:
https://github.com/provanamanish/pbi-scoping-tool

================================================================================
 💡 TIPS & BEST PRACTICES
================================================================================

TIP 1: ONE PAGE AT A TIME
  Scope one page per session - easier to track changes
  Export after each page for documentation

TIP 2: REVIEW YELLOW MATCHES
  Don't assume "Likely match" is correct
  Always verify before rebuilding measures

TIP 3: EXPORT EVERYTHING
  Export results for every page you scope
  Creates audit trail of migration decisions

TIP 4: DOCUMENT MANUAL CHANGES
  If you create a field manually, note it
  Helps future team members understand changes

TIP 5: TEST BEFORE PUBLISHING
  After mapping fields, test the new report
  Verify calculations still work correctly

TIP 6: ASK QUESTIONS
  No question is silly
  Manish is here to help!

================================================================================
 📅 TEAM TIMELINE
================================================================================

RIGHT NOW:
  ✅ Tool is built and working
  ✅ Manish can share it via network access
  🟡 URL: Need to ask Manish

THIS WEEK:
  🟡 Expected: ngrok setup for remote access
  🟡 Expected: Manish shares public link in team chat

NEXT WEEK:
  🟡 Expected: Permanent hosting deployed
  🟡 Expected: Custom domain ready
  🟡 Expected: 24/7 availability

ONGOING:
  ✅ Team can use tool for all migrations
  ✅ Feedback to Manish for improvements
  ✅ Share success stories!

================================================================================
 🎉 LET'S GET STARTED!
================================================================================

Ready to scope your migration?

1. Wait for URL from Manish (via email/Slack/Teams)
2. Bookmark it
3. Follow the Quick Start guide above
4. Export your results
5. Come back to questions in this guide

Your Power BI migrations just got easier! 🚀

================================================================================
 📞 CONTACT & FEEDBACK
================================================================================

Questions about the tool?
  → Ask Manish Kumar Yadav

Bug report or feature request?
  → GitHub issues: https://github.com/provanamanish/pbi-scoping-tool/issues

Need help with Power BI?
  → Check your team's Power BI documentation
  → Ask your Power BI administrator

Found something cool?
  → Share it with the team!

================================================================================
 ✨ TOOL CREATED BY
================================================================================

Developer: Manish Kumar Yadav

Repository: https://github.com/provanamanish/pbi-scoping-tool
License: MIT (free to use and modify)

Questions about how it works?
→ Check the GitHub repository
→ Source code is open and auditable

================================================================================
 🙏 THANK YOU!
================================================================================

Thanks for using the Power BI Field Router!

Your feedback helps us improve the tool.
Questions? Ask Manish.
Enjoying it? Spread the word! 

Happy migrating! 🎉
