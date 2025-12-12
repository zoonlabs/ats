# 🚀 Push to GitHub - Complete Guide

## 📋 **Prerequisites**

### **Step 1: Install Git**

Git is not installed on your system. You need to install it first.

**Download Git for Windows:**
1. Go to: https://git-scm.com/download/win
2. Download the installer
3. Run the installer with default settings
4. Restart your terminal/PowerShell after installation

**Verify installation:**
```bash
git --version
# Should show: git version 2.x.x
```

---

## 🔐 **Step 2: Configure Git**

```bash
# Set your name (will appear in commits)
git config --global user.name "Your Name"

# Set your email (should match your GitHub email)
git config --global user.email "your.email@example.com"

# Verify
git config --global --list
```

---

## 📁 **Step 3: Prepare the Repository**

The `.gitignore` file has been created to exclude:
- ❌ `db.sqlite3` (database - will be recreated)
- ❌ `media/` folder (uploaded resumes - not needed in repo)
- ❌ `.env` file (secrets - never commit!)
- ❌ `__pycache__/` and `*.pyc` (compiled Python)
- ❌ Test scripts (debug_upload.py, check_jobs.py, etc.)
- ❌ Extra documentation (keeping only README and essential docs)

**What WILL be included:**
- ✅ All Django code (`ats/`, `projectname/`)
- ✅ Templates and static files
- ✅ `requirements.txt`
- ✅ `Dockerfile` and `render.yaml`
- ✅ Main documentation (`docs/README.md`, `TESTING_GUIDE.md`, `QUICK_TEST.md`)

---

## 🎯 **Step 4: Initialize Git Repository**

```bash
# Navigate to your project directory
cd C:\Users\mkeer\Desktop\manage

# Initialize git repository
git init

# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status

# Create initial commit
git commit -m "Initial commit: Django ATS with AI-powered candidate scoring"
```

---

## 🌐 **Step 5: Create GitHub Repository**

1. **Go to GitHub:**
   - Visit: https://github.com
   - Login to your account (or create one if needed)

2. **Create New Repository:**
   - Click the "+" icon (top-right) → "New repository"
   - **Repository name:** `django-ats` (or your preferred name)
   - **Description:** "AI-powered Applicant Tracking System with resume parsing and candidate scoring"
   - **Visibility:** Choose Public or Private
   - **DON'T** initialize with README (we already have files)
   - Click "Create repository"

3. **Copy the repository URL:**
   - You'll see: `https://github.com/yourusername/django-ats.git`
   - Or SSH: `git@github.com:yourusername/django-ats.git`

---

## 📤 **Step 6: Push to GitHub**

```bash
# Add GitHub repository as remote
git remote add origin https://github.com/yourusername/django-ats.git

# Push to GitHub (main branch)
git push -u origin main

# Or if it's "master" branch:
git branch -M main  # Rename to main
git push -u origin main
```

**If you get authentication error:**
```bash
# GitHub no longer accepts passwords, use Personal Access Token (PAT)
# 1. Go to: https://github.com/settings/tokens
# 2. Generate new token (classic)
# 3. Select scopes: repo (all)
# 4. Copy the token
# 5. Use token as password when pushing
```

---

## 🔑 **Step 7: Create .env.example (Template for Others)**

Create a template so others know what environment variables are needed:

```bash
# This file is already created below
```

---

## 📝 **Step 8: Update README for GitHub**

The main README should tell visitors:
- What the project does
- How to set it up
- Required environment variables
- How to run it

---

## ✅ **Quick Command Summary**

```bash
# 1. Install Git (download from git-scm.com)

# 2. Configure Git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 3. Initialize repository
cd C:\Users\mkeer\Desktop\manage
git init

# 4. Add files
git add .

# 5. Commit
git commit -m "Initial commit: Django ATS with AI-powered scoring"

# 6. Add remote (replace with your GitHub URL)
git remote add origin https://github.com/yourusername/django-ats.git

# 7. Push
git branch -M main
git push -u origin main
```

---

## 🚨 **IMPORTANT: Before Pushing**

### **Check .env is NOT included:**
```bash
git status | findstr .env
# Should show nothing (means .env is ignored)
```

### **Verify sensitive data is excluded:**
```bash
# Check what will be committed:
git status

# Should NOT see:
# - .env
# - db.sqlite3
# - media/
# - __pycache__/
```

---

## 🎁 **What Others Need to Do After Cloning**

Anyone who clones your repository needs to:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/django-ats.git
cd django-ats

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (copy from .env.example)
copy .env.example .env
# Edit .env and add real API keys

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

---

## 📂 **Repository Structure**

```
django-ats/
├── ats/                      # Main Django app
│   ├── templates/           # HTML templates
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── forms.py            # Forms
│   ├── parsers.py          # Resume parsing
│   ├── scoring.py          # Basic scoring
│   ├── advanced_scoring.py # AI scoring
│   └── urls.py             # URL routing
├── projectname/             # Django project settings
│   ├── settings.py         # Configuration
│   ├── urls.py             # Main URLs
│   └── wsgi.py             # WSGI config
├── docs/                    # Documentation
│   └── README.md           # Main documentation
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── render.yaml             # Render deployment config
├── .gitignore              # Git ignore rules
├── .env.example            # Environment variables template
└── manage.py               # Django management script
```

---

## 🔒 **Security Checklist**

Before pushing, verify:

- [ ] `.env` file is in `.gitignore` ✅
- [ ] No API keys in code ✅
- [ ] `db.sqlite3` is excluded ✅
- [ ] `OPENROUTER_API_KEY` not in committed files ✅
- [ ] `SECRET_KEY` in settings.py uses `env()` ✅

---

## 🎯 **After Pushing**

Your repository will be ready for:
- ✅ Sharing with team members
- ✅ Deployment to Render/Heroku
- ✅ Collaboration and contributions
- ✅ Version control and backups
- ✅ Portfolio showcase

---

## 💡 **Tips**

### **Regular Updates:**
```bash
# After making changes:
git add .
git commit -m "Descriptive message about changes"
git push
```

### **Check Status:**
```bash
git status          # See what's changed
git log --oneline   # See commit history
git diff            # See exact changes
```

### **Create Branches:**
```bash
# For new features:
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

---

## 🆘 **Troubleshooting**

### **"fatal: not a git repository"**
```bash
git init
```

### **"Authentication failed"**
- Use Personal Access Token instead of password
- Or set up SSH keys

### **"rejected - non-fast-forward"**
```bash
git pull origin main --rebase
git push
```

### **Accidentally committed .env**
```bash
# Remove from git but keep locally
git rm --cached .env
git commit -m "Remove .env from repository"
git push
```

---

## ✅ **You're Ready!**

Follow the steps above to push your ATS to GitHub! 🚀

**Need help?** Let me know which step you're on!

