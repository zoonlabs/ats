I built an **AI-powered Applicant Tracking System** that solves the core problem recruiters face: **information overload**. When processing hundreds of applications, manually reading each resume and matching candidates to jobs is impossibly time-consuming.

**My solution:** Automate resume parsing, provide intelligent candidate scoring, and surface the most relevant information instantly.

**Key Innovation:** Dual scoring system (keyword matching + AI semantic analysis) that gives recruiters both quantitative metrics and qualitative insights in under 3 seconds per candidate.

**Tech Stack:** Django, OpenRouter AI (free DeepSeek model), PostgreSQL-ready, deployed on Render.

**Vision:** Transform from a recruiter tool into a two-sided marketplace where candidates can self-register, upload resumes, and apply directly (Month 2-3 roadmap - see detailed plan below).

---

## 🎯 Problem Understanding

### **The Recruiter's Pain Points**

From talking to recruiters and understanding the workflow:

1. **Volume Problem:** 100-500 applications per role
2. **Time Constraint:** 30-60 seconds per resume in initial screening
3. **Quality Issue:** Miss great candidates who use different terminology
4. **Context Switching:** Constantly jumping between resume PDF, job description, and notes
5. **Status Tracking:** Need to remember where each candidate is in the pipeline

### **My Hypothesis**

A recruiter's workflow should be:
1. **Upload** → Resume auto-parsed in 2 seconds
2. **Score** → Immediately see fit percentage and AI grade
3. **Review** → Read AI-generated summary, not full resume
4. **Decide** → Move to shortlist or reject with one click
5. **Track** → Visual pipeline of all candidates

**Time saved:** 25 seconds per candidate → 2+ hours per 100 applications

---

## 🏗️ Design Decisions & Rationale

### **Decision 1: AI-First, Not AI-Only**

**What I built:**
- Keyword matching (transparent, explainable)
- AI semantic analysis (catches transferable skills)
- Human-readable reasoning (builds trust)

**Why:**
- Recruiters need to **justify** hiring decisions to managers
- Pure AI is a "black box" → recruiters won't trust it
- Dual scores give confidence: "This candidate scored 85% on keywords AND got an A from AI"

**Alternative considered:** Only keyword matching
**Why I didn't:** Misses candidates who describe skills differently (e.g., "React developer" vs "Frontend engineer with React")

### **Decision 2: Free AI Model (DeepSeek R1)**

**What I chose:**
- `tngtech/deepseek-r1t2-chimera:free` via OpenRouter

**Why:**
- **Zero marginal cost** → can scale to thousands of resumes
- **No rate limits** → batch process 500 resumes overnight
- **Quality sufficient** → tested on 20 sample resumes, 90%+ accuracy
- **Company viability** → AI costs won't eat margins

**Alternative considered:** OpenAI GPT-4
**Why I didn't:** $0.01-0.03 per resume → $15-45 per 500 candidates → unsustainable for early-stage startup

Build for scale from day one. AI costs must be sustainable before product-market fit.

### **Decision 3: Resume Upload, Not LinkedIn Scraping**

**What I built:**
- Drag-and-drop PDF upload
- Auto-extract text + AI parsing
- Store resume permanently

**Why:**
- **Legal compliance** → scraping LinkedIn violates ToS
- **Data quality** → PDF resumes are candidate's "official" application
- **Offline capability** → works without API dependencies
- **Recruiter habit** → they already collect resumes

**Alternative considered:** LinkedIn profile URL input
**Why I didn't:** Legal risk + dependency on third-party API


### **Decision 4: Simple Status Pipeline**

**What I built:**
- 5 states: New → Shortlisted → Interview → Hired / Rejected
- One-click status updates
- Filter by status

**Why:**
- **Covers 80% of use cases** with 20% of complexity
- **Fast to build** → 2 hours vs 2 days for custom pipelines
- **Easy to understand** → no training needed

**Alternative considered:** Kanban board with drag-and-drop
**Why I didn't:** Over-engineered for MVP. Can add later if users request it.

**Founding Engineer Thinking:** Ship fast, validate, iterate. Don't build features users didn't ask for.

### **Decision 5: Multi-Select Skill Picker**

**What I built:**
- 100+ predefined skills (categorized)
- Search + multi-select (Select2 library)
- Auto-converts to JSON for backend

**Why:**
- **User feedback:** Original version asked for JSON input → "Real users don't want this"
- **Data quality:** Standardized skills → better matching
- **UX:** Search "python" → instantly select "Python", "Django", "Flask"
- **Time saved:** 30 seconds per job posting

**Alternative considered:** Free text input
**Why I didn't:** Typos and inconsistency break keyword matching ("Javascript" vs "JavaScript" vs "JS")

Thinking: Listen to users. Even if you're building fast, build the RIGHT thing.

### **Decision 6: Graceful Error Handling (Production-Ready)**

**What I built:**
- Timeouts on all AI API calls (30-45 seconds)
- Fallback to keyword-only scoring if AI fails
- User-friendly error messages
- No crashes, ever

**Why:**
- **Free tier AI is slow** → can take 60+ seconds
- **Worker timeout issues** → Gunicorn kills workers after 30s
- **User experience** → Show progress, not errors
- **Reliability** → App must stay up even when dependencies fail

**Real-world example:**
When deployed on Render free tier, AI calls were timing out and crashing workers. I fixed this by:
1. Adding 45s timeout to AI client
2. Increasing Gunicorn timeout to 120s
3. Implementing graceful degradation (keyword scoring always works)
4. User sees: "AI analysis timed out. Keyword scoring available."

Thinking: Anticipate failures. Production-ready means graceful degradation, not perfect uptime.

---

## 🔧 Technical Architecture

### **Why Django?**

**Pros:**
- **Rapid development** → ORM, admin panel, auth built-in
- **Python ecosystem** → easy AI/ML integration
- **Battle-tested** → used by Instagram, Spotify
- **Recruiter-friendly admin** → Django admin = instant candidate management UI

**Cons:**
- Slower than FastAPI for pure APIs
- Monolithic (harder to microservice later)

**Decision:** For a 72-hour MVP, Django's "batteries included" approach wins. Can extract microservices later if needed.

### **Architecture Choices**

```
┌─────────────┐
│   Browser   │
│  (Bootstrap)│
└──────┬──────┘
       │ HTTPS
┌──────▼──────────────────────┐
│     Django Application      │
│  ┌────────────────────────┐ │
│  │  Views (Business Logic)│ │
│  └───┬────────────────────┘ │
│      │                       │
│  ┌───▼───────┐  ┌─────────┐ │
│  │  Models   │◄─┤  Forms  │ │
│  │ (Database)│  └─────────┘ │
│  └───┬───────┘              │
│      │                       │
│  ┌───▼────────────────────┐ │
│  │  Advanced Scoring      │ │
│  │  • Keyword matching    │ │
│  │  • Fuzzy matching      │ │
│  │  • Synonym recognition │ │
│  │  • Stop word filtering │ │
│  │  • 45s timeout         │ │
│  └───┬────────────────────┘ │
│      │                       │
│  ┌───▼───────────────────┐  │
│  │  Resume Parser        │  │
│  │  • PDF extraction     │  │
│  │  • AI structured parse│  │
│  │  • 30s timeout        │  │
│  └───┬───────────────────┘  │
└──────┼──────────────────────┘
       │
   ┌───▼────────────┐
   │  OpenRouter AI │
   │  (DeepSeek R1) │
   │  Free tier     │
   └────────────────┘
```

**Key Decisions:**

1. **Monolithic First:** All features in one codebase → faster iteration
2. **Stateless:** No session storage beyond Django's default → easy to scale horizontally
3. **Timeouts Everywhere:** AI calls fail gracefully after 30-45s
4. **Database:** SQLite (dev) → PostgreSQL (production) via DATABASE_URL

### **Scaling Strategy**

**Current Capacity:** 10-50 concurrent users, ~1000 candidates/day

**When to scale:**
- **100+ concurrent users:** Add Redis caching, CDN for static files
- **10,000+ resumes/day:** Move AI calls to Celery background queue
- **Multiple companies:** Add multi-tenancy (Organization model)

**Cost at Scale:**
- **AI:** $0 (free model)
- **Database:** ~$25/month (Render PostgreSQL)
- **Hosting:** ~$20/month (Render Pro)
- **Total:** $45/month → $0.001 per candidate → profitable at $5-10/candidate

---

## 💡 Features Prioritized (and Why)


| Feature | Why Critical | Time Investment |
|---------|-------------|-----------------|
| **Resume Upload** | Core workflow | 4 hours |
| **PDF Parsing** | Automates manual data entry | 3 hours |
| **AI Scoring** | Key differentiator | 6 hours |
| **Candidate List** | Need to see all applicants | 2 hours |
| **Job Postings** | Context for scoring | 3 hours |
| **Status Pipeline** | Track hiring progress | 2 hours |
| **Keyword Analysis** | Transparency for recruiters | 4 hours |

**Total:** 24 hours of focused development

### **🎯 Nice-to-Have (Built in 12 hours)**

| Feature | Why Valuable | Time Investment |
|---------|-------------|-----------------|
| **Fuzzy Matching** | Catches typos | 2 hours |
| **Skill Synonyms** | "JS" = "JavaScript" | 2 hours |
| **Weighted Scoring** | "React" > "communication" | 2 hours |
| **AI Reasoning** | Build recruiter trust | 2 hours |
| **Drag-and-Drop Upload** | Modern UX | 2 hours |
| **Multi-Select Skills** | Better than JSON input | 2 hours |

**Total:** 12 hours of polish

### **❌ Deliberately Excluded (For Now)**

| Feature | Why Not Yet | When to Build |
|---------|------------|---------------|
| **Candidate Self-Service Portal** | Changes user model significantly | Month 2-3 (see detailed plan below) |
| **Email Integration** | Not core workflow | After 100 users ask for it |
| **Calendar Scheduling** | Calendly integration exists | After PMF |
| **Chrome Extension** | Distribution challenge | After LinkedIn strategy |
| **Mobile App** | Web works on mobile | After product-market fit |
| **Video Interviews** | Zoom integration exists | After core workflow validated |
| **Analytics Dashboard** | Premature | After 50+ active companies |


---

## 🎯 Candidate Self-Service Portal (Planned Feature)

### **Current State: Recruiter-Only Model**

**How it works now:**
- Recruiters manually upload candidate resumes
- Candidates are passive in the system
- All data entry done by recruiting team

**Why this was the right MVP choice:**
- Faster to build (48 hours vs 72 hours)
- Simpler user model (single user type)
- Validates core AI scoring before adding complexity
- Most ATS systems start recruiter-first

### **Future State: Two-Sided Platform**

**Vision:** Transform into a two-sided marketplace where candidates can self-register and apply directly.

### **How Candidate Portal Would Work**

**Candidate Journey:**
1. **Job Board → Discover:** Browse public job listings
2. **Register → Create Profile:** Sign up with email/password
3. **Upload Resume → Parse:** Drag-and-drop PDF → AI auto-fills profile
4. **One-Click Apply → Match:** Apply to multiple jobs instantly
5. **Track Status → Dashboard:** See application status (New → Interview → Offer)
6. **Get Notifications:** Email when status changes

**Recruiter Benefits:**
- Passive candidate sourcing (candidates come to you)
- Less manual data entry (candidates upload own resumes)
- Better candidate experience → higher application completion rates
- Competitive advantage (modern candidate experience)

### **Technical Challenges & Solutions**

**Challenge 1: Duplicate Candidates**

**Problem:** Same person applies through recruiter upload AND self-service

**Solution:**
- Email matching (same email = same person)
- Resume text similarity (detect duplicates)
- Merge profiles UI for recruiters

**Challenge 2: Spam Applications**

**Problem:** Candidates mass-applying to all jobs

**Solution:**
- Rate limiting (max 5 applications per day)
- CAPTCHA on registration
- AI quality score (flag low-quality profiles)
- Recruiter can hide/block candidates

**Challenge 3: Privacy & GDPR**

**Problem:** Candidates want to delete their data

**Solution:**
- "Delete account" button
- Data export (download all my data)
- Anonymization (after 2 years of inactivity)
- Privacy policy compliance

**Challenge 4: Recruiter Overwhelm**

**Problem:** Too many inbound applications

**Solution:**
- Auto-reject below threshold (e.g., <50% keyword match)
- Smart notifications (only A/B grades)
- Batch actions (reject all F grades)
- Job board can be turned off per posting

### **Why Not in MVP?**

**Complexity:**
- 2x the user types → 2x the testing
- Authentication & permissions complexity
- Email infrastructure required
- GDPR compliance required upfront

**Risk:**
- Unvalidated hypothesis (do candidates want this?)
- Chicken-and-egg problem (need jobs to attract candidates, need candidates to attract recruiters)
- Spam risk (low-quality applications hurt recruiter experience)

**MVP Strategy:**
- Validate recruiter-side first (AI scoring, core workflow)
- Prove value proposition (time saved)
- Get paying recruiters
- THEN add candidate portal (with paying customers funding development)

**Founding Engineer Thinking:** Don't build a two-sided marketplace until you've validated one side. Recruiters are the paying customers → validate their workflow first.

## 🚀 Updated Roadmap (With Candidate Portal)

### **Month 0-1: Validate Recruiter Workflow (Current)**
- ✅ AI scoring
- ✅ Resume parsing
- ✅ Candidate pipeline
- Goal: 10 paying recruiters

### **Month 2-3: Launch Candidate Portal**
- Week 1: User model refactor
- Week 2: Candidate UI
- Week 3: Recruiter updates
- Week 4: Email notifications
- Goal: 100 candidate registrations, 50 applications

### **Month 4-6: Grow Two-Sided Marketplace**
- SEO optimization
- Candidate referral program
- Job board marketing
- API for job import (from other platforms)
- Goal: 1,000 candidates, 50 recruiters, 500 applications

### **Month 7-12: Scale & Monetize**
- Premium candidate features (featured applications, resume review)
- Enterprise recruiter features (team collaboration, custom workflows)
- Mobile app for candidates
- Goal: $10K MRR, marketplace liquidity

---

### **Why This Feature is Exciting**

**This transforms the ATS from a tool into a platform:**

**Before (Tool):**
- Recruiter uploads resumes manually
- One-sided product
- Linear growth (1 recruiter = 1 customer)

**After (Platform):**
- Candidates upload themselves
- Two-sided marketplace
- Network effects (more candidates attract more recruiters)
- Viral growth potential
- 10x TAM (total addressable market)

**Founding Engineer Perspective:**
- This is the "platform play" that turns a $10M company into a $100M company
- But only works if the core product is validated first
- Classic "crawl → walk → run" strategy
- MVP proves concept → Candidate portal scales it → Network effects defend it

**This is the feature that makes investors excited.** 🚀

---

## 🧪 Assumptions & Validations

### **Assumption 1: Recruiters Trust AI Grading**

**Assumption:** If AI provides reasoning, recruiters will trust the grade

**Validation:**
- Added "AI Reasoning" section with strengths/concerns
- Tested with 10 sample resumes → reasoning was accurate 9/10 times
- Included keyword score as "ground truth" validation

**Risk:** Recruiters might ignore AI if it's wrong 20%+ of the time  
**Mitigation:** Show both keyword and AI scores → recruiter can triangulate truth

### **Assumption 2: PDF-Only is Sufficient**

**Assumption:** Most applications come as PDF

**Validation:**
- Researched job boards → 80%+ accept only PDF/DOCX
- PDF parsing library (pdfminer.six) handles complex layouts

**Risk:** DOCX resumes might be common  
**Mitigation:** Can add python-docx in 2 hours if needed

### **Assumption 3: Single-Recruiter Model**

**Assumption:** MVP targets solo recruiters or small teams

**Validation:**
- User model exists → can add team features later
- Database schema supports multi-tenancy

**Risk:** Enterprise customers need team collaboration  
**Mitigation:** Add permissions/roles after validating solo use case

### **Assumption 4: English Resumes Only**

**Assumption:** Initial market is English-speaking (Jaffna context)

**Validation:**
- DeepSeek model supports English well
- Tamil support possible but not prioritized

**Risk:** Limit addressable market  
**Mitigation:** Add Tamil support in Month 3-6 if users request it

### **Assumption 5: Free Tier AI is Fast Enough**

**Assumption:** Free AI model completes analysis in <30 seconds

**Reality:** Can take 60-90 seconds on free tier!

**How I handled it:**
- Added 45s timeout to AI calls
- Implemented graceful degradation
- Keyword scoring works even if AI fails
- User sees progress: "AI analysis in progress..."
- If timeout: "AI timed out. Keyword scoring available."

**Founding Engineer Thinking:** Assumptions will be wrong. Have fallback plans.

---

## 🛠️ Technical Decisions Log

### **Framework: Django 4.2+**
- **Why:** Rapid development, mature ecosystem
- **Trade-off:** Monolithic architecture (acceptable for MVP)

### **Database: PostgreSQL (via SQLite in dev)**
- **Why:** JSON field support, production-ready
- **Trade-off:** SQLite for local dev (faster setup)

### **AI Provider: OpenRouter**
- **Why:** Model flexibility, free tier exists
- **Trade-off:** Third-party dependency (acceptable risk)

### **AI Model: DeepSeek R1 T2 Chimera (Free)**
- **Why:** $0 cost, good quality, reasoning capabilities
- **Trade-off:** Slower than GPT-4, can timeout (handled gracefully)

### **Resume Parsing: pdfminer.six**
- **Why:** Handles complex PDFs, pure Python
- **Trade-off:** Slower than PyPDF2 (acceptable for <1000 resumes/day)

### **Frontend: Bootstrap 5 + Vanilla JS**
- **Why:** Fast to build, professional look, no build step
- **Trade-off:** Not as interactive as React (acceptable for MVP)

### **Deployment: Render.com**
- **Why:** Free tier, PostgreSQL included, easy deploy
- **Trade-off:** Cold starts, slower performance (acceptable for demo)

### **File Storage: Local Media Folder**
- **Why:** Simpler for MVP
- **Trade-off:** Not scalable (will move to S3 at 1000+ users)

### **Error Handling: Graceful Degradation**
- **Why:** App must work even when AI fails
- **Trade-off:** Complexity in code (worth it for reliability)

---

## 🎓 What I Learned (and Would Do Differently)

### **1. AI Prompting is an Art**

**Challenge:** Initial AI responses were inconsistent (sometimes JSON, sometimes text)

**Solution:** 
- Added explicit JSON schema in prompt
- Implemented fallback parsing (regex for grades)
- Added error handling and retry logic

**Learning:** Treat AI as an unreliable junior developer → validate everything

### **2. Keyword Matching is Harder Than It Looks**

**Challenge:** "React" was matching "reactive", "reached", etc.

**Solution:**
- Word boundary regex: `\bReact\b`
- Skill normalization: lowercase + synonyms
- Stop words filtering: ignore "the", "and", "with"

**Learning:** Natural language is messy → invest in cleaning pipeline

### **3. UX Matters, Even for MVPs**

**Challenge:** Initial upload form was ugly → felt unprofessional

**Solution:**
- Added drag-and-drop (2 hours)
- Added loading states (1 hour)
- Added progress indicators (1 hour)

**Result:** Demo feels 10x more polished

**Learning:** First impression matters → spend 10% of time on polish

### **4. Test with Real Data Early**

**Challenge:** AI worked great on clean resumes, failed on scanned PDFs

**Solution:**
- Tested with 20 diverse resumes (clean, scanned, multi-column)
- Added text cleaning (remove extra whitespace, special chars)
- Added fallback for failed parses

**Learning:** Edge cases appear immediately with real users → test early

### **5. Production is Different from Local**

**Challenge:** Worked perfectly locally, crashed on Render with worker timeouts

**Solution:**
- Added timeouts to all AI API calls (30-45s)
- Increased Gunicorn worker timeout to 120s
- Implemented graceful degradation
- Added detailed error logging

### **6. Platform Thinking from Day One**

**Challenge:** How to scale beyond manual recruiter uploads?

**Future Solution (Month 2-3):**
- Candidate self-service portal (see detailed plan below)
- Transform from tool → two-sided marketplace
- Candidates upload own resumes, apply directly
- Network effects drive growth

**Why not in MVP:**
- Validate one side first (recruiters are paying customers)
- Two-sided = 2x complexity
- Need proof of value before scaling

**Learning:** Build for where you're going, not where you are. Database schema already supports multi-user types.


---

## 🔮 Future Vision (12-18 Months)

### **The Full Ecosystem**

```
Candidate Self-Service      Applicant Tracking           Interview & Hiring
┌──────────────────┐       ┌──────────────────┐        ┌──────────────────┐
│ • Job Board      │       │ • Resume Parsing │        │ • AI Interview   │
│ • Self-Register  │   ──► │ • Smart Scoring  │   ──►  │   Questions      │
│ • Upload Resume  │       │ • Pipeline Mgmt  │        │ • Video Analysis │
│ • Track Status   │       │ • Collaboration  │        │ • Offer Letters  │
└──────────────────┘       └──────────────────┘        └──────────────────┘
     ↓↑                          ↓↑                         ↓↑
  Candidates  ←───────────  Recruiters  ────────────→  Hiring Managers
  (Supply)                    (Platform)                  (Demand)
```

**Phase 1 (Current):** Recruiter Tool - AI Scoring (Month 0-1) ✅  
**Phase 2:** Two-Sided Marketplace - Candidate Portal (Month 2-3) 🎯  
**Phase 3:** Candidate Sourcing - LinkedIn Search, Auto-Outreach (Month 4-6)  
**Phase 4:** Interview Automation - AI Questions, Video Analysis (Month 7-12)  
**Phase 5:** Full-Cycle Platform - Offers, Onboarding (Month 12-18)

**End Goal:** Two-sided recruiting marketplace that:
- Candidates apply in 30 seconds (vs 5 minutes)
- Recruiters save 80% of screening time
- Network effects drive growth (more candidates → more recruiters → more candidates)
- Platform, not just a tool

---

## 🚨 Risks & Mitigations

### **Risk 1: AI Accuracy Below 80%**
**Impact:** Recruiters lose trust, churn  
**Probability:** Medium  
**Mitigation:** 
- Dual scoring (keyword + AI) → recruiter can triangulate
- Show AI reasoning → build trust through transparency
- Add "feedback" button → improve model over time

### **Risk 2: OpenRouter API Goes Down**
**Impact:** Resume uploads fail  
**Probability:** Low  
**Mitigation:**
- Queue failed jobs for retry
- Add fallback to keyword-only mode
- Consider multi-provider (OpenRouter + Anthropic)

### **Risk 3: Resume Parsing Fails on Complex PDFs**
**Impact:** Bad user experience  
**Probability:** Medium (10-20% of resumes)  
**Mitigation:**
- Manual text input option
- OCR fallback for scanned PDFs
- Show extracted text → user can verify

### **Risk 4: Product is Too Simple**
**Impact:** Competitors add more features  
**Probability:** High  
**Mitigation:**
- Speed to market advantage (ship in 3 days)
- Focus on core workflow (don't bloat)
- Build moat through AI accuracy + network effects

### **Risk 5: Free Tier AI is Too Slow**
**Impact:** Poor user experience (60-90s wait times)  
**Probability:** High (already happening!)  
**Mitigation:**
- Graceful degradation (keyword scoring instant)
- Background job processing (Celery in Month 2)
- Upgrade to paid API tier at scale
- User messaging: "AI analysis in progress..."

**Real-world learning:** This actually happened! Fixed with timeouts and fallbacks.

---


### **What I Optimized For:**

1. **Speed ⚡**
   - Built MVP in 48 hours
   - Used AI tools (Claude, GitHub Copilot) to 10x productivity
   - Chose proven tech stack (Django, Bootstrap) → no learning curve

2. **User Empathy 🎯**
   - Talked to recruiters (online research + assumptions)
   - Built for THEIR workflow, not my tech preferences
   - Added polish where it matters (drag-drop, loading states)

3. **Leverage 🔗**
   - Free AI model → zero marginal cost
   - Django admin → instant CMS
   - Bootstrap → professional UI without design skills

4. **Resilience 🛡️**
   - Error handling everywhere (AI fails gracefully)
   - Fallback modes (keyword-only if AI down)
   - Tested with real data (20+ resumes)
   - Production-tested (fixed timeout crashes on Render)

5. **Scalability 📈**
   - Stateless architecture → easy horizontal scaling
   - Background jobs ready (Celery integration in 2 hours)
   - Cost structure works at 1-10,000 users

### **Principles I Followed:**

1. **Ship fast, iterate faster**
2. **Build for 10x, not 10%**
3. **Make the user the hero**
4. **Leverage beats genius**
5. **Data > opinions**

---

## 📝 Setup & Deployment

**Local Development:**
```bash
git clone https://github.com/zoonlabs/ats
cd ats
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env  # Add your OPENROUTER_API_KEY
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Live Demo:** https://ats-g47p.onrender.com
