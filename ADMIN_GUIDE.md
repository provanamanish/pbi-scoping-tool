================================================================================
 📢 ADMIN GUIDE - PUBLISHING & MANAGING TEAM ACCESS
================================================================================

This guide is for YOU (Manish) - the creator and administrator of the tool.

It covers how to prepare, deploy, and manage the tool for your team.

================================================================================
 🎯 YOUR ROLE
================================================================================

You are now the administrator of the Power BI Field Router tool.

Your responsibilities:
  ✅ Keep the tool running (or deployment active)
  ✅ Support team members using the tool
  ✅ Fix bugs or issues
  ✅ Add new features based on feedback
  ✅ Document the tool and its usage
  ✅ Manage access and permissions

Don't worry - the tool is designed to be simple to maintain!

================================================================================
 📋 DEPLOYMENT CHECKLIST - CHOOSE YOUR METHOD
================================================================================

QUICK DEMO (THIS WEEK)
────────────────────────────────────────────────────────────────────────────
☐ Option 1 - Network Access (simplest)
  ☐ Share: http://IDAP-VM2:5000/ (or http://172.20.240.102:5000/)
  ☐ Prerequisites: Computer on, Flask running
  ☐ Good for: Quick team demo
  ☐ Duration: Days to weeks
  
☐ Option 2 - ngrok Setup (5 min)
  ☐ Download ngrok from https://ngrok.com/download
  ☐ Extract and run: ngrok http 5000
  ☐ Copy HTTPS URL
  ☐ Share URL with team via email/Slack
  ☐ Good for: Demo across internet
  ☐ Duration: Hours to days (limited free tier)

PERMANENT DEPLOYMENT (NEXT 1-2 WEEKS)
────────────────────────────────────────────────────────────────────────────
☐ Option 1 - PythonAnywhere (Recommended)
  See: DEPLOYMENT_TO_DOMAIN.md → Option 2
  ☐ Time to setup: 15 minutes
  ☐ Cost: Free or $5/month
  ☐ URL: https://username.pythonanywhere.com
  ☐ Custom domain: Extra $10/year
  
☐ Option 2 - Railway (Modern)
  See: DEPLOYMENT_TO_DOMAIN.md → Option 3
  ☐ Time to setup: 20 minutes
  ☐ Cost: Free tier or $5/month
  ☐ URL: Automatic or custom
  
☐ Option 3 - Render (Free tier)
  See: DEPLOYMENT_TO_DOMAIN.md → Option 4
  ☐ Time to setup: 20 minutes
  ☐ Cost: Free (with limitations)
  ☐ URL: https://name.onrender.com

BEST CHOICE FOR YOUR SITUATION: PythonAnywhere
  • Easiest Flask setup
  • Free tier works fine for team
  • Can add custom domain later
  • 24/7 availability

================================================================================
 🚀 STEP-BY-STEP: SETUP PYTHONANYWHERE TODAY
================================================================================

This will take about 20 minutes and give your team permanent access.

PART 1: CREATE ACCOUNT (3 minutes)
────────────────────────────────────────────────────────────────────────────
1. Go to: https://www.pythonanywhere.com
2. Click: "Create free account"
3. Username: Choose something like "manish" or "manish-pbi"
4. Email: Your email
5. Password: Strong password
6. Verify email

PART 2: UPLOAD YOUR CODE (5 minutes)
────────────────────────────────────────────────────────────────────────────
1. Log in to PythonAnywhere
2. Click: "Files" (top navigation)
3. Click: "Upload a file"
4. Upload these files:
   ☐ app.py
   ☐ pbi_inspect.py
   ☐ requirements.txt
   ☐ test_field_router.py

5. Files will be in: /home/yourusername/

PART 3: CREATE WEB APP (3 minutes)
────────────────────────────────────────────────────────────────────────────
1. Click: "Web" (top navigation)
2. Click: "Add a new web app"
3. Choose: "Python 3.9" (or latest)
4. Choose: "Flask"
5. Path: /home/yourusername/app.py
6. Click: "Next"

PART 4: CONFIGURE WSGI (5 minutes)
────────────────────────────────────────────────────────────────────────────
1. PythonAnywhere opens WSGI config file
2. Delete everything
3. Paste this:

import sys
path = '/home/yourusername'
if path not in sys.path:
    sys.path.append(path)
from app import app as application

4. Replace "yourusername" with YOUR PythonAnywhere username
5. Save (Ctrl+S)

PART 5: INSTALL DEPENDENCIES (2 minutes)
────────────────────────────────────────────────────────────────────────────
1. Click: "Consoles" (top navigation)
2. Click: "Bash" → "Create new bash console"
3. Type:
   pip install flask pandas openpyxl

4. Wait for installation to complete

PART 6: RELOAD AND TEST (2 minutes)
────────────────────────────────────────────────────────────────────────────
1. Go back to: "Web"
2. Find green "Reload" button
3. Click it
4. Wait for it to reload
5. Go to: https://yourusername.pythonanywhere.com/
6. You should see your tool with your name in the corner!

PART 7: TEST WITH TEAM (Optional)
────────────────────────────────────────────────────────────────────────────
1. Open the tool
2. Verify it works (upload test files, if you have them)
3. Copy URL
4. Send to team in Slack/email

DONE! ✅

Your team can now access: https://yourusername.pythonanywhere.com/

================================================================================
 📧 MESSAGE TO SHARE WITH TEAM
================================================================================

Copy and send this to your team:

────────────────────────────────────────────────────────────────────────────
Subject: PBI Scoping Tool Now Available!

Hi everyone,

The Power BI Field Router tool is now live and ready for our migration project!

What it does:
✅ Automatically maps fields from old to new Power BI reports
✅ Identifies missing or renamed fields
✅ Exports mapping results as CSV or Excel
✅ Saves hours of manual mapping work

Access it here: https://yourusername.pythonanywhere.com/

How to use:
1. Upload old and new .pbix files
2. Select a page to map
3. Review results and download

No installation needed - just open the link in your browser!

Questions? Ask me.

Thanks,
Manish
────────────────────────────────────────────────────────────────────────────

================================================================================
 🛠️  ONGOING MAINTENANCE
================================================================================

DAILY CHECKLIST:
  ☐ Tool is accessible (try opening the URL)
  ☐ Team reports no errors
  ☐ No issues in team chat

WEEKLY:
  ☐ Check for team feedback
  ☐ Make note of feature requests
  ☐ Monitor tool usage (if available)

MONTHLY:
  ☐ Update requirements if needed (pip list)
  ☐ Merge any improvements to code
  ☐ Review error logs (if available)

QUARTERLY:
  ☐ Major version releases
  ☐ New features based on feedback
  ☐ Performance optimization

================================================================================
 🐛 TROUBLESHOOTING - FOR YOU
================================================================================

TEAM REPORTS: "Tool is down"
  → Check if PythonAnywhere web app is running
  → Check "Web" → "Reload" button status
  → If red: Click reload
  → Check if error log shows issues (Web → Error log)

TEAM REPORTS: "Files won't upload"
  → Check file upload limit on PythonAnywhere
  → May need to upgrade account for larger files

TEAM REPORTS: "Tool is slow"
  → Check if many people using simultaneously
  → PythonAnywhere free tier has CPU limits
  → May need to upgrade plan or use Railway

TEAM REPORTS: "Feature XYZ doesn't work"
  → Reproduce issue locally first
  → Check pbi_inspect.py for bugs
  → Fix locally and test
  → Deploy updated app.py to PythonAnywhere

================================================================================
 ⬆️  UPGRADING THE TOOL
================================================================================

When you make improvements to the code:

STEP 1: Test locally
  python3.14 app.py
  (Make sure it works)

STEP 2: Commit to GitHub
  git add .
  git commit -m "Description of changes"
  git push origin main

STEP 3: Deploy to PythonAnywhere
  1. Go to "Files" on PythonAnywhere
  2. Delete old app.py
  3. Upload new app.py
  4. Go to "Web" → Click "Reload"

Done! ✅ Team gets new version immediately

================================================================================
 📊 MONITORING TEAM USAGE (Optional)
================================================================================

PythonAnywhere free tier doesn't show detailed usage stats, but you can:

View Error Logs:
  Web → Error log
  (Shows if team encounters errors)

Manual Tracking:
  ☐ Ask team periodically: "Is tool working?"
  ☐ Keep note of feature requests
  ☐ Collect feedback via email/form

Later (if upgrading to paid):
  ☐ Get server logs
  ☐ See request metrics
  ☐ Monitor performance

================================================================================
 💰 COST BREAKDOWN
================================================================================

Current Setup (Recommended):
  PythonAnywhere free tier:    $0/month
  Domain name (optional):       $10-12/year (~$1/month)
  ────────────────────────────
  Total:                         $0-1/month

Upgrade later (if needed):
  PythonAnywhere Premium tier:  $5/month
  Better performance, higher limits

Enterprise (not needed now):
  AWS / Railway:                $10-50+/month
  Only if thousands of users

================================================================================
 🔒 SECURITY FOR ADMINS
================================================================================

Important security reminders:

✅ DO:
  • Keep PythonAnywhere password strong
  • Enable 2FA (Two-Factor Authentication) on account
  • Backup code locally (already done via GitHub)
  • Review team access (though tool is public by default)
  • Monitor error logs for attacks

❌ DON'T:
  • Share your PythonAnywhere password
  • Commit secrets to GitHub (already prevented via .gitignore)
  • Run untrusted code on the server
  • Leave sensitive files on the server
  • Give team direct server access

Current Security Status: ✅ GOOD
  • No credentials in code
  • Files processed locally (not stored)
  • HTTPS enabled automatically
  • No database or data persistence

================================================================================
 📚 DOCUMENTATION FOR YOU
================================================================================

Keep these files for reference:

Repository:
  https://github.com/provanamanish/pbi-scoping-tool

Guides in this folder:
  ✅ README.md                     (Project overview)
  ✅ QUICKSTART.md                 (5-min user guide)
  ✅ TEAM_ONBOARDING.md            (For your team)
  ✅ DEPLOYMENT_TO_DOMAIN.md       (Deployment options)
  ✅ NGROK_QUICK_START.md          (Quick public access)
  ✅ DEPLOYMENT_GUIDE.md           (Full deployment)
  ✅ SHARING_GUIDE.md              (Network sharing)
  ✅ GIT_SETUP_GUIDE.md            (Git reference)
  ✅ SECURITY_AUDIT.md             (Security review)
  ✅ BUILD_SUMMARY.md              (Architecture)
  ✅ PROJECT_COMPLETION_CHECKLIST.md (Feature list)
  ✅ TEST_RESULTS.md               (Test coverage)

================================================================================
 🎓 ADVANCED: CUSTOMIZING FOR YOUR ORGANIZATION
================================================================================

Want to customize the tool further? You can:

CHANGE THE NAME:
  Edit app.py → INDEX_HTML → <h1> tag
  Change "Field Router" to your company name

CHANGE COLORS:
  Edit app.py → INDEX_HTML → :root section
  Modify CSS color variables

ADD YOUR COMPANY LOGO:
  Add logo.png to project
  Edit HTML to include logo in sidebar

ADD TEAM CONTACT:
  Edit app.py → startup message
  Add "For support: manish@company.com"

ADD USAGE TRACKING:
  Integrate analytics (Plausible, Fathom, etc.)
  Track team usage patterns

More advanced features coming in future versions!

================================================================================
 ✨ YOU'RE ALL SET!
================================================================================

Your Power BI Field Router is ready to empower your team!

Next steps:
  1. Choose deployment method (PythonAnywhere recommended)
  2. Follow setup steps above
  3. Share URL with team
  4. Celebrate! 🎉

Timeline:
  Today: Setup and deploy (1 hour)
  This week: Team using it
  This month: Feedback and improvements
  This quarter: New features based on needs

Remember:
  • You built this - be proud!
  • Your team will love it
  • Keep iterating based on feedback
  • Have fun! 🚀

Questions about deployment?
→ Check DEPLOYMENT_TO_DOMAIN.md
→ Read PythonAnywhere documentation
→ Search GitHub for similar Flask projects

Questions about the code?
→ Check source code comments
→ Review pbi_inspect.py functions
→ Read BUILD_SUMMARY.md

Ready? Let's deploy! 🚀

================================================================================
 📞 QUICK REFERENCE
================================================================================

Important URLs:
  Your repo: https://github.com/provanamanish/pbi-scoping-tool
  PythonAnywhere: https://www.pythonanywhere.com
  ngrok: https://ngrok.com
  Your deployed tool: https://yourusername.pythonanywhere.com

Commands you'll need:
  git status                          # Check status
  git add .                          # Stage changes
  git commit -m "message"            # Commit
  git push origin main               # Push to GitHub
  python3.14 app.py                  # Run locally

Team communication:
  Share deployment URL with team
  Keep it updated in team wiki/docs
  Announce new features

Support:
  Team questions: Reply with link to TEAM_ONBOARDING.md
  Bug reports: Update code, test, deploy new version
  Feature requests: Add to issues list

================================================================================
 🏆 SUCCESS CRITERIA
================================================================================

You'll know you've succeeded when:

  ✅ Team can access tool without installation
  ✅ Team can upload two .pbix files
  ✅ Tool runs without errors
  ✅ Results are accurate (spot-check one page)
  ✅ Team downloads results successfully
  ✅ Team understands the confidence scores
  ✅ Team saves time on field mapping
  ✅ Team gives positive feedback

Celebrate these wins! 🎉

================================================================================
 🚀 LET'S DO THIS!
================================================================================

Your tool is production-ready.
Your team will love it.
Let's go! 🚀

Manish, you've got this! 💪
