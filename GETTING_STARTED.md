# 🚀 Power BI Field Router - Getting Started

**Welcome!** This guide will get you using the Power BI Field Router tool in minutes.

---

## ⚡ Quick Start (5 Minutes)

### **Step 1: Start the Tool**

#### **Option A: PowerShell (Recommended)**
```powershell
.\START_TOOL.ps1
```

#### **Option B: Command Line (Windows)**
```cmd
START_TOOL.bat
```

#### **Option C: Manual (Any OS)**
```bash
python3.13 app.py
```

### **Step 2: Open in Browser**

When the server starts, you'll see something like:
```
🚀 POWER BI FIELD ROUTER - SCOPING TOOL
📍 Local Access:    http://127.0.0.1:5000
🌐 Network Access:  http://172.20.240.102:5000
💻 Computer Name:   http://IDAP-VM2:5000
```

**Copy and paste one of these links into your browser:**
- Use `http://127.0.0.1:5000` if using on THIS machine only
- Use `http://172.20.240.102:5000` to share with team on same network
- Use `http://IDAP-VM2:5000` to access by computer name

### **Step 3: Upload Your Reports**

1. Click the "Old report" box → Choose your OLD .pbix file
2. Click the "New report" box → Choose your NEW .pbix file
3. Click "Analyze reports" button
4. Wait 30-60 seconds for analysis to complete

### **Step 4: Select Page & Review Results**

1. Choose a page from the dropdown (sorted by importance)
2. Look at the page preview (shows field count, hidden status, etc.)
3. Review the results table:
   - 🟢 **Green** = Safe to use (exact or likely match)
   - 🟡 **Yellow** = Review before using (partial match)
   - 🔴 **Red** = Will need manual creation (missing field)

### **Step 5: Export & Share**

1. Click "Download CSV" or "Download Excel"
2. Save the file
3. Share with your team or stakeholders

---

## 📚 Understanding Results

### **Confidence Scores**

| Score | Meaning | Action |
|-------|---------|--------|
| 🟢 100% | Exact match | Use as-is ✓ |
| 🟢 82-99% | Likely match | Review, usually safe |
| 🟡 60-81% | Possible match | Review carefully |
| 🟡 0-59% | Weak match | Likely needs manual work |
| ❌ 0% | No match | Field missing, create manually |

### **Color Meanings**

- **🟢 Green** - Everything looks good
- **🟡 Yellow** - Something to review
- **🔴 Red** - Missing field, needs attention

---

## 💡 Tips & Tricks

### **Pro Tips**
✓ Do one page at a time - easier to review  
✓ Export after each page for documentation  
✓ Use Search box to filter results by field name  
✓ Share results in Excel for stakeholder review  
✓ Keep old results for comparison

### **Troubleshooting**

**"Analyze reports" button is greyed out**
- Make sure you've selected BOTH old AND new files
- Files must be .pbix (Power BI) format

**"Connection refused" or "page won't load"**
- Make sure tool is still running (check terminal window)
- Try refreshing browser (F5)
- Copy-paste URL from terminal

**Results look odd / low confidence**
- This is normal! Field names often differ between reports
- Review yellow matches manually
- Check for naming style differences (CamelCase vs snake_case vs spaces)

**Tool seems slow**
- Large reports take time to analyze (30-60 seconds is normal)
- Wait for the spinning indicator to stop
- Don't close the browser tab while processing

---

## 🔄 Workflow Example

### **Scenario: Migrating Report to New Workspace**

1. **Setup**: Tool already running at `http://127.0.0.1:5000`

2. **Prepare Files**:
   - Get OLD report (.pbix file) from original workspace
   - Get NEW report (.pbix file) from new workspace

3. **Upload**:
   - Drag & drop or click to select OLD report
   - Drag & drop or click to select NEW report
   - Click "Analyze reports"

4. **Process**:
   - Tool automatically extracts all fields
   - Builds field matching database
   - Shows results in 30-60 seconds

5. **Review**:
   - Select each page one by one
   - Check green (exact) matches
   - Review yellow (possible) matches
   - Note red (missing) fields

6. **Export**:
   - Download Excel with full mapping
   - Share with team for manual field creation
   - Keep for documentation

7. **Create**:
   - Your dev team uses export to create missing fields
   - Reference mapping for any ambiguous matches

---

## 📊 What You'll See

### **Upload Step** (Step 1)
- Two file upload boxes
- Instructions for selecting files
- Analyze button (enabled when both files selected)
- Help panel on right with tips

### **Page Selection** (Step 2)
- Dropdown with all pages
- Page preview showing:
  - 📄 Page name
  - 📊 Number of fields
  - ⚠️ Hidden status
  - 🎯 Page type
- Help panel with guidance

### **Results** (Step 3)
- Summary showing total matches/missing
- Search box to filter results
- Table with columns:
  - Old table name
  - Old field name
  - Field type (Measure, Column, etc)
  - Match status (Exact, Likely, etc)
  - New table name
  - New field name
  - Confidence % (0-100)
  - Notes
  - DAX expression (if available)
- Export buttons (CSV/Excel)

---

## 🔐 Security & Privacy

✅ **Your files never leave this machine**
- Everything processes locally
- No data sent to internet
- No cloud storage
- Works offline

✅ **Safe to use with sensitive reports**
- No credentials stored
- No external connections
- Open source (you can review code)

---

## 🆘 Need Help?

### **Check These First**
1. Read the help panel on right side (changes with each step)
2. Look at the "Need Help?" section for common issues
3. Review the tips & tricks above

### **Common Questions**

**Q: Can I use this with Power BI Desktop?**
A: No, you need .pbix exported files. But you can use it without Power BI Desktop installed.

**Q: Do I need internet?**
A: No, works completely offline after starting the server.

**Q: Can I run this on a different computer?**
A: Yes! Use the network link (http://172.20.240.102:5000 or similar) to share with team.

**Q: How long does analysis take?**
A: Typically 30-60 seconds depending on report size.

**Q: Can I stop and restart?**
A: Yes! Press CTRL+C in terminal to stop, then run START_TOOL.ps1 to restart.

---

## 🎯 Next Steps

1. **Start the tool** - Run `.\START_TOOL.ps1`
2. **Open browser** - Navigate to `http://127.0.0.1:5000`
3. **Upload reports** - Select your .pbix files
4. **Review results** - Check field mappings
5. **Export data** - Download CSV or Excel
6. **Share with team** - Collaborate on mapping

---

## 📞 Support

For questions or issues:
- Check the help panel on the right (it changes based on your step)
- Review this guide
- Check the TEAM_ONBOARDING.md for more details
- Refer to README.md for technical information

---

**Made with ❤️ by Manish Kumar Yadav**

Happy field mapping! 🚀
