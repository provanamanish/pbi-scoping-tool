================================================================================
 🌐 DEPLOYMENT GUIDE - PUBLISH WITH CUSTOM DOMAIN
================================================================================

Your Power BI Field Router tool is ready to be deployed and shared with your
entire team using a domain name!

This guide covers multiple deployment options, from quick (ngrok) to
production-grade (custom domain).

================================================================================
 📋 QUICK COMPARISON
================================================================================

┌─────────────────┬────────────┬──────────────┬─────────────────┬──────────┐
│ Option          │ Setup Time │ Cost         │ Domain Support  │ Uptime   │
├─────────────────┼────────────┼──────────────┼─────────────────┼──────────┤
│ ngrok           │ 5 min      │ Free         │ Random URL      │ Temporary│
│ PythonAnywhere  │ 15 min     │ Free/Paid    │ Custom domain   │ 24/7     │
│ Railway         │ 20 min     │ Free trial   │ Custom domain   │ 24/7     │
│ Render          │ 20 min     │ Free tier    │ Custom domain   │ 24/7     │
│ AWS + Route53   │ 30 min     │ Pay-as-you-go│ Custom domain   │ 24/7     │
└─────────────────┴────────────┴──────────────┴─────────────────┴──────────┘

BEST FOR TEAM USE: PythonAnywhere or Railway (custom domain + free tier)

================================================================================
 🚀 OPTION 1: NGROK (INSTANT PUBLIC ACCESS - NO DOMAIN)
================================================================================

⏱️  Setup Time: 5 minutes
💰 Cost: Free (or paid for custom domain)
✅ Best for: Quick team sharing

Perfect for immediately sharing with team without setup!

STEP 1: Download ngrok
────────────────────────────────────────────────────────────────────────────
1. Go to: https://ngrok.com/download
2. Download for Windows
3. Extract to a folder (e.g., C:\ngrok)

STEP 2: Start your Flask server
────────────────────────────────────────────────────────────────────────────
PowerShell:
  cd "c:\Users\manishkumar.yadav\Downloads\Scoping Tool"
  python3.14 app.py

(Keep this terminal open)

STEP 3: In another PowerShell, start ngrok
────────────────────────────────────────────────────────────────────────────
  cd C:\ngrok
  .\ngrok http 5000

OUTPUT (you'll see something like):
  Forwarding    https://abc123def456.ngrok.io -> http://localhost:5000

STEP 4: Share the URL with your team
────────────────────────────────────────────────────────────────────────────
  Copy: https://abc123def456.ngrok.io
  
  Tell your team: "Access the tool at: https://abc123def456.ngrok.io"

Note: URL changes each time you restart. For custom domain, use paid ngrok.

================================================================================
 🌍 OPTION 2: PYTHONANYWHERE (RECOMMENDED FOR TEAMS)
================================================================================

⏱️  Setup Time: 15 minutes
💰 Cost: Free tier available
✅ Best for: Permanent team access with custom domain
✅ Pros: Simple Flask hosting, free tier works, can add custom domain

STEP 1: Create free account
────────────────────────────────────────────────────────────────────────────
1. Go to: https://www.pythonanywhere.com/
2. Click "Sign up"
3. Choose free account (pythonanywhere.com subdomain included)
4. Verify email

STEP 2: Upload your code
────────────────────────────────────────────────────────────────────────────
1. Log in to PythonAnywhere
2. Files → Upload files
3. Upload:
   - app.py
   - pbi_inspect.py
   - requirements.txt
   - test_field_router.py
4. Create folder structure: /home/USERNAME/pbi-scoping-tool/

STEP 3: Create Web app
────────────────────────────────────────────────────────────────────────────
1. Web → Add a new web app
2. Choose "Python 3.9" (or latest available)
3. Choose "Flask"
4. Path: /home/USERNAME/pbi-scoping-tool/app.py

STEP 4: Configure WSGI file
────────────────────────────────────────────────────────────────────────────
1. Web → WSGI configuration file
2. Edit the file that opens

Replace contents with:
────────────────────────────────────────────────────────────────────────────
import sys
path = '/home/USERNAME/pbi-scoping-tool'
if path not in sys.path:
    sys.path.append(path)

from app import app as application

────────────────────────────────────────────────────────────────────────────

3. Replace USERNAME with your PythonAnywhere username

STEP 5: Install dependencies
────────────────────────────────────────────────────────────────────────────
1. Consoles → Bash console
2. Navigate: cd /home/USERNAME/pbi-scoping-tool
3. Install: pip install flask pandas openpyxl

Note: pbixray may not work on free tier (optional feature)

STEP 6: Reload web app
────────────────────────────────────────────────────────────────────────────
1. Web → Reload button
2. Your app is live at: https://USERNAME.pythonanywhere.com

STEP 7: Add custom domain (optional, requires paid account)
────────────────────────────────────────────────────────────────────────────
1. Web → Security → Custom domain
2. Add your domain
3. Point DNS to PythonAnywhere
4. Follow their instructions

URL for team: https://USERNAME.pythonanywhere.com

================================================================================
 🚂 OPTION 3: RAILWAY (MODERN & EASY)
================================================================================

⏱️  Setup Time: 20 minutes
💰 Cost: Free trial $5/month, then pay-as-you-go
✅ Best for: Modern Python hosting with custom domain support

STEP 1: Create Railway account
────────────────────────────────────────────────────────────────────────────
1. Go to: https://railway.app
2. Sign up (GitHub recommended)
3. Create new project

STEP 2: Connect your GitHub repo
────────────────────────────────────────────────────────────────────────────
1. In Railway: Add service → GitHub Repo
2. Select: provanamanish/pbi-scoping-tool
3. Railway auto-detects Flask app
4. Confirm deployment

STEP 3: Set environment variables
────────────────────────────────────────────────────────────────────────────
1. Variables tab
2. Add:
   FLASK_ENV = production
   PORT = 5000

STEP 4: Deploy
────────────────────────────────────────────────────────────────────────────
1. Click "Deploy"
2. Wait for build to complete
3. Get public URL from "Domains"

STEP 5: Add custom domain (requires paid account)
────────────────────────────────────────────────────────────────────────────
1. Settings → Custom Domain
2. Add your domain (e.g., pbi-router.yourcompany.com)
3. Follow DNS setup
4. Done!

URL for team: https://your-railway-domain.railway.app

================================================================================
 📦 OPTION 4: RENDER (FREE TIER + CUSTOM DOMAIN)
================================================================================

⏱️  Setup Time: 20 minutes
💰 Cost: Free tier available (with limitations)
✅ Best for: Simple deployment with free tier

STEP 1: Create Render account
────────────────────────────────────────────────────────────────────────────
1. Go to: https://render.com
2. Sign up with GitHub

STEP 2: Create new Web Service
────────────────────────────────────────────────────────────────────────────
1. Dashboard → New Web Service
2. Connect to GitHub: provanamanish/pbi-scoping-tool
3. Name: pbi-scoping-tool
4. Environment: Python
5. Build Command: pip install -r requirements.txt
6. Start Command: gunicorn app:app

STEP 3: Add to requirements.txt
────────────────────────────────────────────────────────────────────────────
Add this line to requirements.txt (if not present):
  gunicorn>=20.0.0

STEP 4: Environment variables
────────────────────────────────────────────────────────────────────────────
1. Environment tab
2. Add: FLASK_ENV = production

STEP 5: Deploy
────────────────────────────────────────────────────────────────────────────
1. Click Deploy
2. Wait ~5 minutes
3. Get URL when done

STEP 6: Custom domain
────────────────────────────────────────────────────────────────────────────
1. Settings → Custom Domain
2. Add domain
3. Update DNS records
4. Done!

URL for team: https://pbi-scoping-tool-yourname.onrender.com

================================================================================
 ☁️  OPTION 5: AWS + ROUTE53 (PRODUCTION GRADE)
================================================================================

⏱️  Setup Time: 30 minutes
💰 Cost: Pay-as-you-go (~$5-20/month)
✅ Best for: Professional, high-reliability deployment

STEP 1: Create AWS account
────────────────────────────────────────────────────────────────────────────
1. Go to: https://aws.amazon.com/
2. Sign up
3. Verify identity

STEP 2: Use Elastic Beanstalk
────────────────────────────────────────────────────────────────────────────
1. Search: Elastic Beanstalk
2. Create application → Flask
3. Upload your code as ZIP
4. Configure environment

STEP 3: Get domain on Route 53
────────────────────────────────────────────────────────────────────────────
1. Route 53 → Registered domains
2. Register domain (e.g., pbi-scoping-tool.com)
3. Create DNS record pointing to Beanstalk

STEP 4: Launch
────────────────────────────────────────────────────────────────────────────
1. Deploy
2. Get environment URL
3. Add custom domain

URL for team: https://pbi-scoping-tool.yourcompany.com

Note: This requires AWS knowledge. Consider PythonAnywhere or Railway first.

================================================================================
 🎯 RECOMMENDED PATH FOR YOUR TEAM
================================================================================

IMMEDIATE (This week):
  1. Use ngrok (5 min) to demo with team
  2. Tell team the URL (changes on restart, but free)
  3. Works perfectly for internal testing

SHORT-TERM (Next 1-2 weeks):
  1. Deploy to PythonAnywhere (free tier)
  2. Add custom domain option later
  3. Permanent URL: https://yourname.pythonanywhere.com

LONG-TERM (When ready):
  1. Buy custom domain (GoDaddy, Namecheap, etc.)
  2. Switch to Railway or AWS
  3. Use domain like: https://pbi-router.yourcompany.com

================================================================================
 📝 STEP-BY-STEP: SET UP WITH PYTHONANYWHERE TODAY
================================================================================

This is the fastest way to get permanent team access!

1. Create free PythonAnywhere account: https://pythonanywhere.com
   (5 minutes)

2. Upload your files (10 minutes):
   Files → Upload all project files

3. Create Flask web app (5 minutes):
   Web → Add app → Flask → Python 3.9

4. Install dependencies:
   Bash console → pip install flask pandas openpyxl

5. Reload:
   Web → Green Reload button

6. Get your team URL:
   https://USERNAME.pythonanywhere.com/

That's it! Share the URL with your team.

================================================================================
 🔐 SECURITY CONSIDERATIONS
================================================================================

Before publishing, ensure:

✅ No .pbix files uploaded to hosting
✅ No credentials in environment
✅ HTTPS only (all options above use HTTPS)
✅ File upload size limits set
✅ Regular backups of logs
✅ Only trusted team members have access

================================================================================
 🆘 TROUBLESHOOTING
================================================================================

Issue: "ModuleNotFoundError: No module named 'pbi_inspect'"
Solution: Make sure all .py files uploaded together in same directory

Issue: "pbixray not available"
Solution: Install with: pip install pbixray
         (May not work on free tiers due to C dependencies)

Issue: "Port already in use"
Solution: Hosting service assigns port automatically, not your concern

Issue: "File upload too slow"
Solution: ngrok/Railway may throttle. Use PythonAnywhere for better limits.

Issue: "Can't access from team network"
Solution: Make sure it's HTTPS not HTTP. Some corporate firewalls block.

================================================================================
 📞 GET HELP
================================================================================

PythonAnywhere:
  https://www.pythonanywhere.com/help/

Railway:
  https://docs.railway.app/

Render:
  https://docs.render.com/docs

ngrok:
  https://ngrok.com/docs

================================================================================
 ✅ NEXT STEPS
================================================================================

1. IMMEDIATE (now):
   ☐ Run Flask app locally: python3.14 app.py
   ☐ Test at: http://127.0.0.1:5000
   ☐ Verify your name shows in bottom right corner

2. TODAY:
   ☐ Choose deployment option (recommended: PythonAnywhere)
   ☐ Create account on platform
   ☐ Upload files

3. THIS WEEK:
   ☐ Get public URL
   ☐ Test with team
   ☐ Share URL in team communication

4. OPTIONAL - LATER:
   ☐ Buy custom domain
   ☐ Update DNS
   ☐ Migrate to production platform

================================================================================
 🎉 YOU'RE READY!
================================================================================

Your Power BI Field Router is production-ready and secure.

Choose PythonAnywhere for the easiest team deployment, or contact your
infrastructure team if you need AWS deployment.

Happy scaling! 🚀
