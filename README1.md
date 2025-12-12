# 🚀 AI-Powered Applicant Tracking System (ATS)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-DeepSeek%20R1-purple.svg)](https://openrouter.ai/)

A modern, AI-powered Applicant Tracking System built with Django that automatically parses resumes, matches candidates to jobs, and provides intelligent scoring.

## ✨ Features

### 🤖 **AI-Powered Intelligence**
- **Resume Parsing**: Automatically extracts contact info, skills, experience, and education from PDF resumes
- **Semantic Matching**: Deep AI analysis of candidate-job fit beyond simple keyword matching
- **Dual Scoring System**: 
  - Keyword matching score (0-100%)
  - AI grade (A-F) with detailed reasoning
- **Free AI Model**: Uses `tngtech/deepseek-r1t2-chimera:free` - no API costs!

### 📊 **Advanced Scoring Features**
- **Stop Words Filtering**: Removes common words for accurate matching
- **Skill Normalization**: Recognizes skill variations (e.g., "JS" = "JavaScript")
- **Weighted Scoring**: Prioritizes important skills over generic keywords
- **Fuzzy Matching**: Partial credit for similar skills (e.g., "developer" ~ "development")
- **AI Semantic Analysis**: Evaluates transferable skills and overall fit

### 💼 **Recruiter-Friendly Interface**
- **Dashboard**: Quick metrics and recent activity
- **Job Management**: Create, edit, and manage job postings
- **Candidate Pipeline**: Track candidates through hiring stages (New → Shortlisted → Interview → Hired/Rejected)
- **Multi-Select Skill Picker**: No JSON editing - search and select from 100+ predefined skills
- **Drag-and-Drop Upload**: Modern file upload interface
- **Keyword Analysis**: See matched and missing keywords at a glance
- **AI Insights**: View AI reasoning, strengths, concerns, and recommendations

### 🎨 **Modern UI/UX**
- Bootstrap 5 design with custom styling
- Loading states and toast notifications
- Progress bars and visual score indicators
- Color-coded AI grades
- Responsive and mobile-friendly
- Avatar circles and status badges

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- OpenRouter API key (free tier available)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/django-ats.git
cd django-ats

# 2. Create virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
copy .env.example .env
# Edit .env and add your OpenRouter API key

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

Visit `http://localhost:8000` and login with your superuser credentials!

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# OpenRouter API (Required for AI features)
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_APP_NAME=ATS-Application
```

**Get your free API key:**
1. Visit [OpenRouter.ai](https://openrouter.ai/keys)
2. Sign up for a free account
3. Generate an API key
4. The free model (`tngtech/deepseek-r1t2-chimera:free`) has no usage costs!

## 📖 Usage

### Creating a Job Posting

1. Navigate to **Jobs → Create Job**
2. Enter job title and detailed description
3. Use the **skill picker** to select required skills (search from 100+ options)
4. Submit to create the posting

### Uploading Candidates

1. Navigate to **Candidates → Upload Candidate**
2. Select the job position
3. Enter candidate name (email/phone optional - will be auto-extracted)
4. **Drag and drop** PDF resume or click to browse
5. Click "Upload & Analyze Resume"

**What happens next:**
- ✅ PDF text extraction
- ✅ AI parsing (skills, experience, education, contact info)
- ✅ Keyword matching against job description
- ✅ AI semantic analysis (2-3 seconds)
- ✅ Dual scores generated (keyword % + AI grade)
- ✅ Recommendations provided

### Viewing Candidate Details

Click any candidate to see:
- **Dual Scores**: Keyword percentage and AI letter grade
- **Matched Keywords**: Skills present in resume
- **Missing Keywords**: Skills to look for in interview
- **Fuzzy Matches**: Similar skills found
- **AI Analysis**: 
  - Technical skills score
  - Experience level score
  - Overall reasoning
  - Key strengths
  - Concerns to address
  - Hiring recommendation
- **Resume Text**: Full extracted text
- **Status Management**: Change hiring stage

## 🏗️ Architecture

### Tech Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (dev) / PostgreSQL (production)
- **AI/ML**: OpenRouter API (DeepSeek R1 T2 Chimera)
- **PDF Parsing**: pdfminer.six
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Deployment**: Docker-ready, Render.com compatible

### Project Structure

```
django-ats/
├── ats/                        # Main application
│   ├── models.py              # JobPost, Candidate models
│   ├── views.py               # View logic
│   ├── forms.py               # Django forms
│   ├── parsers.py             # PDF parsing with AI
│   ├── scoring.py             # Basic keyword scoring
│   ├── advanced_scoring.py    # AI-powered advanced scoring
│   ├── templates/             # HTML templates
│   │   ├── base.html         # Base template with navbar
│   │   ├── dashboard.html    # Dashboard metrics
│   │   ├── jobs/             # Job-related templates
│   │   └── candidates/       # Candidate-related templates
│   └── urls.py               # URL routing
├── projectname/               # Project settings
│   ├── settings.py           # Django configuration
│   └── urls.py               # Main URL configuration
├── docs/                      # Documentation
├── requirements.txt           # Python dependencies
├── Dockerfile                # Docker configuration
└── render.yaml               # Render deployment config
```

## 🎯 Key Components

### Resume Parsing (`ats/parsers.py`)

```python
def parse_resume(file_obj, filename=None):
    """
    Extracts text from PDF and uses AI to parse structured data.
    Returns: {
        'text': str,
        'email': str,
        'phone': str,
        'skills': list,
        'experience': float,
        'education': str
    }
    """
```

### Advanced Scoring (`ats/advanced_scoring.py`)

```python
def advanced_score_resume(resume_text, job_description, use_ai=True):
    """
    Comprehensive scoring with:
    - Stop words filtering
    - Skill normalization
    - Weighted scoring
    - Fuzzy matching
    - AI semantic analysis
    
    Returns: {
        'keyword_score': int,      # 0-100%
        'ai_score': int,           # 0-100
        'ai_grade': str,           # A-F
        'ai_reasoning': str,
        'matched_keywords': list,
        'missing_keywords': list,
        'fuzzy_matches': dict
    }
    """
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t django-ats .

# Run container
docker run -p 8000:8000 --env-file .env django-ats
```

## 🌐 Production Deployment

### Render.com (Recommended)

1. Connect your GitHub repository to Render
2. Configure environment variables in Render dashboard
3. Deploy automatically on push to main branch

See `render.yaml` for configuration details.

### Environment Variables for Production

```env
SECRET_KEY=<generate-strong-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://...
OPENROUTER_API_KEY=sk-or-v1-...
```

## 📊 Database Models

### JobPost

```python
- title: CharField
- description: TextField
- required_skills: JSONField (list of skills)
- owner: ForeignKey(User)
- created_at: DateTimeField
```

### Candidate

```python
- job: ForeignKey(JobPost)
- name: CharField
- email: EmailField
- phone: CharField
- skills: JSONField
- experience_years: FloatField
- education: TextField
- resume_file: FileField
- resume_text: TextField
- status: CharField (new/shortlisted/interview/hired/rejected)

# Scoring fields
- score: FloatField (legacy keyword score)
- keyword_score: FloatField (advanced keyword score)
- ai_score: FloatField (AI overall score)
- ai_grade: CharField (A-F grade)
- ai_reasoning: TextField
- matched_keywords: TextField
- missing_keywords: TextField
- fuzzy_matches: JSONField

- created_at: DateTimeField
```

## 🧪 Testing

```bash
# Run Django tests
python manage.py test

# Test API connection
python test_api_connection.py

# Test scoring logic
python test_ai_scoring.py
```

## 🔧 Development

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes
3. Test thoroughly
4. Commit: `git commit -m "Add new feature"`
5. Push: `git push origin feature/new-feature`
6. Create Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use Django best practices
- Comment complex logic
- Write descriptive commit messages

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenRouter.ai** for providing free AI model access
- **DeepSeek** for the R1 T2 Chimera reasoning model
- **Django** community for the excellent framework
- **Bootstrap** for the UI components

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## 📸 Screenshots

### Dashboard
![Dashboard with metrics and recent jobs](docs/screenshots/dashboard.png)

### Job Create
![Job creation with multi-select skill picker](docs/screenshots/job-create.png)

### Candidate Upload
![Drag-and-drop candidate upload](docs/screenshots/candidate-upload.png)

### Candidate Detail
![Candidate scores and AI analysis](docs/screenshots/candidate-detail.png)

---

**Built with ❤️ using Django and AI**

⭐ Star this repo if you find it useful!

