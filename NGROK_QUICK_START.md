================================================================================
 ⚡ QUICK NGROK SETUP - SHARE WITH TEAM IN 5 MINUTES
================================================================================

Want to demo the tool with your team RIGHT NOW?
Use ngrok for instant public access!

================================================================================
 📥 STEP 1: DOWNLOAD NGROK
================================================================================

Option A: Download directly
  1. Go to: https://ngrok.com/download
  2. Click "Windows" (64-bit)
  3. Extract the ZIP file
  4. Place ngrok.exe in a folder (e.g., C:\ngrok)

Option B: Via Chocolatey
  choco install ngrok

Option C: Via Scoop
  scoop install ngrok

================================================================================
 🚀 STEP 2: START YOUR APP & NGROK
================================================================================

Terminal 1 - Start Flask Server:
────────────────────────────────────────────────────────────────────────────
  cd "c:\Users\manishkumar.yadav\Downloads\Scoping Tool"
  python3.14 app.py

You should see:
  🚀 POWER BI FIELD ROUTER - SCOPING TOOL
  ======================================
  📍 Local Access (this machine):
     http://127.0.0.1:5000
  🌐 Network Access (share with others):
     http://172.20.240.102:5000
     (keep this terminal OPEN)

Terminal 2 - Start ngrok:
────────────────────────────────────────────────────────────────────────────
  C:\ngrok\ngrok http 5000

You should see:
  ngrok                                                                 
  Session Status                online                                
  Account                       Limited                             
  Version                       3.3.0                               
  Region                        US (Iowa)                           
  Forwarding                    https://xxxx-xxxx-xxx.ngrok.io -> ...
  Forwarding                    http://xxxx-xxxx-xxx.ngrok.io -> ...

Copy the HTTPS URL (first one)

================================================================================
 ✅ STEP 3: SHARE WITH YOUR TEAM
================================================================================

Send this message to your team:

  Hi team! 👋
  
  I've created a Power BI Field Router tool to help with our migration scoping.
  
  📌 Access here: https://xxxx-xxxx-xxx.ngrok.io/
  
  (Replace xxxx-xxxx-xxx with the URL from ngrok)
  
  What it does:
  ✅ Upload old & new Power BI reports
  ✅ Automatically match fields between versions
  ✅ Export mapping results as CSV/Excel
  
  Note: This link works for the next few hours. I'll restart it daily or
  set up permanent hosting soon.
  
  Questions? Ask me!

================================================================================
 ⚙️  KEEP IT RUNNING
================================================================================

The ngrok URL stays alive as long as:
  1. Your laptop is on
  2. Flask server is running (Terminal 1)
  3. ngrok is running (Terminal 2)

To stop:
  Press Ctrl+C in either terminal

To restart with a NEW URL:
  Close both terminals
  Repeat Step 2
  (You'll get a new ngrok URL each time)

================================================================================
 💡 MAKE NGROK PERSISTENT (OPTIONAL)
================================================================================

Want the same URL every time? Use paid ngrok:
  1. Go to: https://ngrok.com/
  2. Sign up ($5/month gets custom domain)
  3. After payment, you can use: ngrok http 5000 --authtoken YOUR_TOKEN
  4. Same URL every restart!

Or just use new URL each time (still free!).

================================================================================
 🆘 TROUBLESHOOTING NGROK
================================================================================

"Address already in use"
  → Another app is using port 5000
  → Solution: python3.14 app.py uses different port
  → Command: python3.14 -c "from app import app; app.run(port=5001)"
  → Then: ngrok http 5001

"Connection refused"
  → Flask server not running
  → Make sure Terminal 1 shows: "Running on http://127.0.0.1:5000"

"ngrok command not found"
  → ngrok not in PATH
  → Solution: Use full path: C:\ngrok\ngrok http 5000

"ERR_NGROK_120"
  → ngrok session limit exceeded
  → Wait a few minutes or upgrade account

================================================================================
 🌐 ALTERNATIVES TO NGROK
================================================================================

If ngrok doesn't work, try:

1. EXPOSE: https://expose.dev/
2. LOCALHOST.RUN:
   ssh -R 80:127.0.0.1:5000 ssh.localhost.run
3. CLOUDFLARE TUNNEL: https://developers.cloudflare.com/cloudflare-one/

But ngrok is easiest for most teams!

================================================================================
 📊 AFTER NGROK WORKS
================================================================================

Once your team is happy with the tool, set up permanent hosting:
  ➡️  See: DEPLOYMENT_TO_DOMAIN.md
  ➡️  Recommended: PythonAnywhere (15 min setup, free tier)

================================================================================
 ✨ YOU'RE ALL SET!
================================================================================

Your team can now:
  1. Open the ngrok URL in their browser
  2. Upload old & new .pbix files
  3. Select a page
  4. Get instant field mappings
  5. Download as CSV or Excel

Enjoy! 🚀

Questions about the tool? See README.md or QUICKSTART.md
