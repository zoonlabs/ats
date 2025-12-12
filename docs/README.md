# ATS – Applicant Tracking System

## Overview
A Django-based Applicant Tracking System for recruiters to manage job postings and hundreds of applications efficiently. Features include authentication, job and candidate management, resume parsing, scoring, status pipeline, dashboard metrics, and a Bootstrap 5 UI. Ready for deployment on Render.

## Features
- User authentication (Django auth)
- CRUD for job postings
- Candidate upload with resume parsing (PDF/DOCX)
- Candidate scoring based on job description keywords
- Status pipeline for candidates
- Sorting/filtering on candidate list
- Dashboard metrics
- Bootstrap 5 UI
- Render deployment-ready

## How to Run Locally
1. Clone the repo and `cd` into the project folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (create a `.env` file in the project root):
   ```bash
   # Django Configuration
   SECRET_KEY=your-secret-key-here-change-in-production
   DEBUG=True
   
   # OpenRouter API Configuration (Required)
   OPENROUTER_API_KEY=your-openrouter-api-key-here
   OPENROUTER_APP_NAME=ATS-Application
   
   # Database (Optional - defaults to SQLite)
   # DATABASE_URL=postgres://user:password@localhost:5432/dbname
   ```
   
   **📝 Get your OpenRouter API Key:**
   1. Visit [https://openrouter.ai](https://openrouter.ai)
   2. Sign up for a free account (GitHub login available)
   3. Go to **Keys** section in dashboard
   4. Click **Create Key** and copy it
   5. Paste into `.env` file above
   
   **💡 Why OpenRouter?**
   - ✅ Better pricing than direct OpenAI
   - ✅ Access to multiple AI models (OpenAI, Anthropic, Google, etc.)
   - ✅ Automatic failover and load balancing
   - ✅ Pay-as-you-go, no subscriptions
   - ✅ Free credits for new users

4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Start the server:
   ```bash
   python manage.py runserver
   ```
7. Access at [http://localhost:8000](http://localhost:8000)

## Resume Parsing Decisions
- **PDF:** Uses pdfminer.six to extract text.
- **AI-Powered:** OpenRouter API (GPT-4o-mini) intelligently extracts:
  - Email addresses
  - Phone numbers
  - Skills list
  - Years of experience
  - Education background

## Advanced Scoring System
The ATS uses a **dual-scoring** approach for maximum accuracy:

### 1. Keyword Score (Fast - 0.1s)
- **Stop Words Filtering:** Removes common words ("the", "and", etc.)
- **Skill Normalization:** Recognizes synonyms (e.g., "JS" = "JavaScript", "Postgres" = "PostgreSQL")
- **Weighted Scoring:** Technical skills weighted 3x, tools 2x, general terms 1x
- **Fuzzy Matching:** Partial credit for similar words (e.g., "developer" ~ "development")

### 2. AI Semantic Score (Deep - 2-3s)
- **Contextual Analysis:** AI understands transferable skills and experience level
- **Letter Grade:** A (Excellent) to F (Poor) recommendation
- **Detailed Reasoning:** Explains strengths, concerns, and hiring recommendation
- **Smart Matching:** Recognizes that Flask experience helps with Django, etc.

**Example Results:**
- Keyword Score: 78% (enhanced keyword matching)
- AI Grade: B+ (contextual fit analysis)

## OpenRouter Configuration
This application uses [OpenRouter](https://openrouter.ai) instead of direct OpenAI API for several benefits:
- **Cost Effective:** Pay-as-you-go with competitive pricing
- **Multiple Models:** Access to OpenAI, Anthropic, Google, DeepSeek, and more
- **Reliability:** Automatic fallback and load balancing
- **No Vendor Lock-in:** Easy to switch between AI providers

**Current AI Model:**
- **DeepSeek R1 T2 Chimera FREE** (`tngtech/deepseek-r1t2-chimera:free`)
  - 🎉 **COMPLETELY FREE** - No API costs!
  - Advanced reasoning model optimized for complex analysis
  - Excellent at understanding context and nuance
  - Superior performance for candidate evaluation tasks
  - Same quality as paid version, community-hosted

**Alternative Models Available:**
- `openai/gpt-4o-mini` - Fast and cheap, good quality
- `openai/gpt-4o` - Most capable OpenAI model
- `anthropic/claude-3-sonnet` - Excellent reasoning
- `meta-llama/llama-3-70b` - Open source, very cheap
- And 100+ more at [openrouter.ai/models](https://openrouter.ai/models)

To change the AI model, edit `ats/parsers.py` (line ~38) and `ats/advanced_scoring.py` (line ~474) and replace `'tngtech/deepseek-r1t2-chimera:free'` with your preferred model.

### 🎉 Why the FREE Version is Perfect

**Zero Cost Benefits:**
- 💰 **$0 per candidate** - Process unlimited resumes at no cost
- 🚀 **Production ready** - Same quality as paid models
- 📊 **For 10,000 candidates: $0** vs $30-40 with paid APIs
- ✅ **No credit card required** - Just sign up for OpenRouter
- 🔄 **No usage limits** (community-hosted, fair use applies)

**Perfect for:**
- 🏢 Small businesses and startups
- 🎓 Testing and development
- 📈 High-volume recruiting (100+ candidates/day)
- 💡 Proof of concept projects

## Deployment (Render)
- Uses Dockerfile and render.yaml for deployment.
- PostgreSQL database provisioned by Render.
- Environment variables managed in render.yaml.

## File Structure
- `ats/` – Django app with models, views, forms, parsers, scoring, templates
- `projectname/` – Django project config
- `requirements.txt`, `Dockerfile`, `render.yaml` – Deployment files

## Feature Explanation
- **Dashboard:** Metrics and recent jobs
- **Jobs:** List, create, detail (with candidate table)
- **Candidates:** Upload, list (sortable/filterable), detail (resume, fields, scoring, status update)
- **Authentication:** Login/logout, protected views
- **Bootstrap 5:** Clean, responsive UI

---

For more details, see the code and comments in each file.
