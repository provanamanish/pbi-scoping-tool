# 🚀 Upload to GitHub - Step-by-Step Guide

## **Step 1: Install Git** (if not already installed)

### Option A: Download from Website (Recommended)
1. Go to https://git-scm.com/download/win
2. Download the latest version
3. Run the installer
4. Accept all defaults
5. Click "Finish"

### Option B: Using Chocolatey (if installed)
```powershell
choco install git -y
```

### Option C: Using Winget (Windows 11)
```powershell
winget install Git.Git
```

**Verify installation:**
```powershell
git --version
# Should show: git version 2.x.x.windows.x
```

---

## **Step 2: Create GitHub Repository**

1. Go to https://github.com/new
2. Enter repository name: `pbi-scoping-tool` (or your preferred name)
3. Add description: `Power BI Field Router - Scoping Tool`
4. Choose **Public** or **Private**
5. Do NOT check "Initialize this repository..."
6. Click **"Create repository"**

After creation, GitHub will show you commands. Copy your repository URL:
```
https://github.com/YOUR_USERNAME/pbi-scoping-tool.git
```

---

## **Step 3: Initialize Git Locally**

Open PowerShell and run these commands:

```powershell
# Navigate to project directory
cd "c:\Users\manishkumar.yadav\Downloads\Scoping Tool"

# Initialize git repository
git init

# Configure git (one-time setup)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Power BI Field Router with fancy UI and network sharing"

# Add remote repository (replace URL with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/pbi-scoping-tool.git

# Verify remote was added
git remote -v
# Should show:
# origin  https://github.com/YOUR_USERNAME/pbi-scoping-tool.git (fetch)
# origin  https://github.com/YOUR_USERNAME/pbi-scoping-tool.git (push)

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## **Alternative: One-Command Setup Script**

Create a file named `git-setup.ps1` with this content:

```powershell
# Git Setup Script for PBI Scoping Tool
$RepoUrl = Read-Host "Enter your GitHub repository URL (https://github.com/...)"
$UserName = Read-Host "Enter your Git username (for commits)"
$UserEmail = Read-Host "Enter your Git email"

cd "c:\Users\manishkumar.yadav\Downloads\Scoping Tool"

# Initialize
git init
git config user.name $UserName
git config user.email $UserEmail

# Add and commit
git add .
git commit -m "Initial commit: Power BI Field Router with fancy UI and network sharing"

# Push
git remote add origin $RepoUrl
git branch -M main
git push -u origin main

Write-Host "✅ Repository created and pushed to GitHub!"
Write-Host "Your repository: $RepoUrl"
```

Then run:
```powershell
.\git-setup.ps1
```

---

## **Step 4: Verify Upload**

1. Go to your GitHub repository URL
2. You should see all your files:
   - app.py
   - pbi_inspect.py
   - test_field_router.py
   - requirements.txt
   - Documentation files
   - START_TOOL.ps1
   - START_TOOL.bat
   - etc.

---

## **Step 5: Future Updates**

To push future changes:

```powershell
cd "c:\Users\manishkumar.yadav\Downloads\Scoping Tool"

# Check what changed
git status

# Add changes
git add .

# Commit
git commit -m "Your commit message describing changes"

# Push to GitHub
git push
```

---

## **Troubleshooting**

### "Git command not found"
- Git not installed
- Solution: Download from https://git-scm.com/download/win

### "fatal: not a git repository"
- You're not in the project directory
- Solution: Run `cd "c:\Users\manishkumar.yadav\Downloads\Scoping Tool"`

### "fatal: authentication failed"
- GitHub credentials issue
- Solution: Use Personal Access Token instead of password:
  1. Go to https://github.com/settings/tokens
  2. Create new token with "repo" scope
  3. Use token instead of password

### "fatal: remote origin already exists"
- Remote already added
- Solution: Remove and re-add:
  ```powershell
  git remote remove origin
  git remote add origin https://github.com/YOUR_USERNAME/pbi-scoping-tool.git
  ```

---

## **Files That Will Be Uploaded**

✅ **Source Code:**
- `app.py` (Flask web application)
- `pbi_inspect.py` (Power BI analysis library)
- `test_field_router.py` (Test suite)

✅ **Configuration:**
- `requirements.txt` (Python dependencies)
- `.gitignore` (Git ignore rules)

✅ **Startup Scripts:**
- `START_TOOL.ps1` (PowerShell starter)
- `START_TOOL.bat` (Batch starter)

✅ **Documentation:**
- `README.md` (Project overview)
- `QUICKSTART.md` (Quick start guide)
- `DEPLOYMENT_GUIDE.md` (Deployment instructions)
- `SHARING_GUIDE.md` (How to share with team)
- `QUICK_SHARE.txt` (Quick reference)
- `PROJECT_COMPLETION_CHECKLIST.md` (Feature checklist)
- `BUILD_SUMMARY.md` (Architecture details)
- `TEST_RESULTS.md` (Test results)

❌ **NOT Uploaded (in .gitignore):**
- `.venv/` (Virtual environment)
- `__pycache__/` (Python cache)
- `*.pbix` files (Power BI files)
- Session data
- Temporary files

---

## **Next Steps After Upload**

1. **Share the GitHub link** with your team
2. **Others can clone:**
   ```powershell
   git clone https://github.com/YOUR_USERNAME/pbi-scoping-tool.git
   cd pbi-scoping-tool
   python3.14 -m pip install -r requirements.txt
   python3.14 app.py
   ```

3. **Collaborate:**
   - Team members can fork and submit pull requests
   - Track issues
   - Manage releases

---

## **Important: GitHub Setup Tips**

### For Private Repository (Recommended):
- Only you and invited collaborators can access
- Go to Settings → Security → Change visibility

### For Public Repository:
- Anyone can view the code
- Great for open-source projects

### Add Collaborators:
1. Go to Settings → Collaborators → Add people
2. Invite team members
3. They can push changes directly

---

**Ready to upload? Follow the steps above!** 🚀

For help, visit:
- Git Guide: https://git-scm.com/doc
- GitHub Guide: https://docs.github.com/en/get-started
