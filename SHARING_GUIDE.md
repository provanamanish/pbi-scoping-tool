# 🔗 How to Share the Power BI Field Router Tool

Your Power BI Field Router tool can now be easily shared with colleagues and team members. Here's how to do it:

---

## **3 Ways to Access & Share the Tool**

### **1️⃣ Local Machine Only (Single User)**
```
http://127.0.0.1:5000
```
- Accessible only on this computer
- Used when you're working alone
- Files stay on your machine

---

### **2️⃣ Network Access (Same LAN) - ⭐ RECOMMENDED**
```
http://172.20.240.102:5000
```
- Share this link with colleagues on the **same network**
- They can access from their computers
- All files processed on YOUR machine
- Works on company networks, VPNs, etc.

**How to find the network IP:**
- Look at the startup message when the tool starts
- It shows: "🌐 Network Access (share with others): http://[YOUR_IP]:5000"

---

### **3️⃣ Computer Name (Optional)**
```
http://IDAP-VM2:5000
```
- Use if network IP is unstable
- Replace "IDAP-VM2" with your actual computer name
- Useful for cross-network access

---

## **Quick Share Steps**

### **Step 1: Start the Tool**
```powershell
cd "c:\Users\manishkumar.yadav\Downloads\Scoping Tool"
.\START_TOOL.ps1
```

When the server starts, you'll see:
```
======================================================================
 🚀 POWER BI FIELD ROUTER - SCOPING TOOL
======================================================================

📍 Local Access (this machine):
   http://127.0.0.1:5000

🌐 Network Access (share with others):
   http://172.20.240.102:5000

💻 Computer Name:
   http://IDAP-VM2:5000
```

### **Step 2: Copy the Shareable Link**
- Open the tool in your browser
- At the top, you'll see **"🔗 SHAREABLE LINK"** banner
- Click **"📋 Copy Link"** button
- Link is now copied to clipboard!

### **Step 3: Share with Colleagues**
- Paste the link in:
  - Email
  - Slack/Teams message
  - Chat
  - Share drive
  - Collaboration tool

### **Step 4: Colleagues Access**
1. Colleagues click the link
2. Tool opens in their browser
3. They can upload their Power BI reports
4. Files are uploaded to YOUR machine (not theirs)
5. They see results in real-time

---

## **Important Security Notes**

⚠️ **What colleagues can access:**
- ✅ Upload their .pbix files to your machine
- ✅ Run field routing analysis
- ✅ Download results
- ✅ View the UI

⚠️ **What colleagues CANNOT access:**
- ❌ Your files on disk
- ❌ Your computer's other data
- ❌ Each other's uploaded files (different sessions)
- ❌ Previous analysis results (cleared on upload)

---

## **Network Access Requirements**

For the tool to work across the network:

✅ **Both computers must be on:**
- Same company network, OR
- Same VPN connection, OR
- Same home/office WiFi, OR
- Connected via direct network link

❌ **Won't work across:**
- Internet (unless you use ngrok)
- Different networks/VPNs
- Behind corporate firewalls (may need admin approval)

---

## **Troubleshooting Shared Access**

### **Issue: Colleague can't access the tool**

**Check 1:** Verify server is running
```powershell
# You should see this on your machine:
 * Running on http://172.20.240.102:5000
```

**Check 2:** Verify network connection
- Both on same network? Run `ipconfig` to check IP
- Can ping? Have colleague run: `ping 172.20.240.102`

**Check 3:** Check firewall
- Port 5000 may be blocked
- Admin may need to allow port 5000
- Try using computer name instead: `http://IDAP-VM2:5000`

**Check 4:** Restart the tool
```powershell
.\START_TOOL.ps1
```

---

## **Advanced Sharing Options**

### **Option A: Using ngrok (Internet-Wide Access)**

For sharing outside your network:

1. **Install ngrok:**
   ```powershell
   choco install ngrok
   # OR download from https://ngrok.com/download
   ```

2. **Start ngrok tunnel:**
   ```powershell
   ngrok http 5000
   ```

3. **Share the public URL:**
   ```
   https://xxxxx.ngrok.io  (example)
   ```

**Benefits:** Works from anywhere in the world
**Warning:** Anyone with the link can access

---

### **Option B: VPN Connection**

1. Both users connect to company VPN
2. Share the network IP: `http://172.20.240.102:5000`
3. Works reliably across offices/remote workers

---

### **Option C: Cloud Deployment** (Advanced)

Deploy to cloud platforms:
- Azure (App Service)
- AWS (EC2)
- Heroku
- Google Cloud

**Note:** Requires system admin setup, not covered here

---

## **Session Management**

Each person gets their own session:

✅ **Colleague 1:**
- Uploads reports → Gets session_id_123
- Analyzes pages → Results stored in session
- Downloads results

✅ **Colleague 2:**
- Uploads reports → Gets session_id_456
- Analyzes pages → Results stored in session
- Downloads results

**Sessions don't interfere with each other!**

---

## **Stopping the Tool**

When you're done sharing:

```powershell
# In the terminal, press:
CTRL+C

# Output:
KeyboardInterrupt
Shutting down...
```

All colleagues will lose access at that moment.

---

## **Tips for Smooth Sharing**

1. **Keep it running:** Leave the tool running while colleagues use it
2. **Monitor performance:** Large .pbix files take time to process
3. **Clear temp files:** Occasionally restart to clean up sessions
4. **Test first:** Have a colleague test before wide rollout
5. **Document the process:** Share these instructions with users

---

## **File Upload Limits**

- **Max file size:** Depends on available disk space
- **Max concurrent users:** 5-10 (depends on network speed)
- **Typical analysis time:** 2-5 seconds per page
- **File storage:** Temporary only (cleaned up after download)

---

## **What Happens Behind the Scenes**

When a colleague uses the tool:

1. **Upload** → Their .pbix files go to YOUR machine temporarily
2. **Process** → Analysis happens on YOUR machine
3. **Results** → Returned to their browser
4. **Cleanup** → Files deleted from your machine after 24 hours

---

## **Support & Help**

If colleagues have questions:

**Quick FAQ:**
- Q: "Is my data safe?" → A: Yes, only processed locally, not sent to cloud
- Q: "Can I access your files?" → A: No, only your uploaded files are visible
- Q: "Will this slow down my computer?" → A: Minimal impact, runs in background
- Q: "How long does analysis take?" → A: Usually 2-5 seconds per page

**Refer them to:**
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for full instructions
- [README.md](README.md) for project overview

---

## **Next Steps**

✅ **Start the server**
```powershell
.\START_TOOL.ps1
```

✅ **Copy the shareable link from the banner**
- Click "📋 Copy Link" button in the UI

✅ **Share with colleagues**
- Email/Slack/Teams the link

✅ **They can start using immediately!**

---

**🎉 Your Power BI Field Router is now shareable!**

Colleagues can now easily:
- 📤 Upload their Power BI reports
- 🔍 Route fields between reports  
- 📥 Export results to CSV/Excel
- ✅ Collaborate on field mapping

**Happy routing! 🚀**
