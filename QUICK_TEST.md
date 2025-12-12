# ⚡ Quick Test Guide - 3 Simple Steps

## 🎉 **NOW USING FREE AI MODEL** - Zero Cost! 💰

## 🚀 Fastest Way to Test (30 seconds)

```bash
# Step 1: Check if API works
python test_api_connection.py

# Step 2: Test scoring with 4 sample candidates
python test_ai_scoring.py
```

**Done!** You'll see:
- ✅ 4 different candidates scored
- ✅ Keyword scores (0-100%)
- ✅ AI grades (A-F)
- ✅ Detailed reasoning for each

---

## 🌐 Test Through Web Interface (2 minutes)

```bash
# Step 1: Create sample jobs
python create_test_data.py

# Step 2: Start server
python manage.py runserver

# Step 3: Open browser and login
http://localhost:8000
```

Then:
1. Go to **Jobs** → Pick any job
2. Click **"Upload Candidate"**
3. Upload any PDF resume
4. ✨ Watch AI analyze in 2-3 seconds!

---

## 📊 What You'll See

### Keyword Score
```
🔍 Keyword Match Score
███████████░░░░ 78%
Enhanced keyword matching with fuzzy logic
```

### AI Analysis
```
🤖 AI Semantic Score
████████████░░ 85% (B+)
AI-powered contextual analysis

💡 AI Analysis:
Strong Python foundation with 6 years experience.
Django expertise matches requirements perfectly...

💪 Strengths:
• Exceeds experience requirement (6 vs 5 years)
• PostgreSQL expertise matches needs
• Proven REST API development

⚠️ Concerns:
• No Kubernetes experience mentioned
• Limited AWS Lambda knowledge

🎯 Recommendation: Recommend - Strong candidate
```

---

## ✅ Success Checklist

Your AI scoring is working if:
- [x] Different candidates get different scores
- [x] AI provides specific reasoning
- [x] Strengths and concerns are listed
- [x] Letter grades (A-F) are assigned
- [x] Response time is under 6 seconds

---

## ❌ Troubleshooting

**"AI analysis not available"**
→ Check `.env` has `OPENROUTER_API_KEY=your-key`
→ Get key from: https://openrouter.ai/keys

**"API call failed"**
→ Run: `python test_api_connection.py`
→ Check you have credits in OpenRouter account

**Resume not parsing**
→ Make sure PDF is text-based (not scanned image)
→ Use the provided `sample_resume.txt` to create a test PDF

---

## 📁 Test Files Created

- `test_api_connection.py` - Check API works
- `test_ai_scoring.py` - Test scoring logic
- `create_test_data.py` - Create sample jobs
- `sample_resume.txt` - Sample resume content
- `TESTING_GUIDE.md` - Detailed guide
- `QUICK_TEST.md` - This file

---

## 🎯 Quick Commands Reference

```bash
# Check API
python test_api_connection.py

# Test scoring
python test_ai_scoring.py

# Create test jobs
python create_test_data.py

# Start server
python manage.py runserver

# Create superuser (if needed)
python manage.py createsuperuser
```

---

**That's it! Start with `python test_api_connection.py` 🚀**

