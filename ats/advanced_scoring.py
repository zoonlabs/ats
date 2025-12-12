"""
Advanced Resume Scoring System
Provides enhanced keyword matching and AI-powered semantic analysis
"""
import re
import json
from difflib import SequenceMatcher
from openai import OpenAI
from django.conf import settings


# Initialize OpenRouter client with timeout
client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL,
    timeout=45.0,  # 45 second timeout for API calls
    max_retries=0,  # No retries to fail fast
)


# ============================================================================
# ENHANCEMENT #1: STOP WORDS FILTERING
# ============================================================================

# Common English stop words that should be ignored in scoring
STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'been', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to',
    'was', 'will', 'with', 'we', 'you', 'your', 'have', 'had', 'this', 'or',
    'but', 'not', 'can', 'could', 'should', 'would', 'may', 'might', 'must',
    'our', 'their', 'his', 'her', 'they', 'them', 'these', 'those', 'who',
    'which', 'what', 'where', 'when', 'why', 'how', 'all', 'each', 'every',
    'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'too', 'very', 'into', 'through', 'about', 'between', 'during', 'before',
    'after', 'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under',
    'again', 'further', 'then', 'once', 'here', 'there', 'also', 'any', 'same',
}


def tokenize(text):
    """
    Extract words from text, convert to lowercase.
    """
    if not text:
        return []
    return re.findall(r'\w+', text.lower())


def filter_stop_words(tokens):
    """
    Remove common stop words from a list of tokens.
    
    Args:
        tokens: List of word tokens
        
    Returns:
        List of tokens with stop words removed
    """
    return [token for token in tokens if token not in STOP_WORDS]


def tokenize_and_filter(text):
    """
    Tokenize text and remove stop words in one step.
    
    Args:
        text: Input text string
        
    Returns:
        List of meaningful tokens (stop words removed)
    """
    tokens = tokenize(text)
    return filter_stop_words(tokens)


# ============================================================================
# ENHANCEMENT #2: SKILL SYNONYMS & NORMALIZATION
# ============================================================================

# Mapping of skill variations to their canonical form
SKILL_SYNONYMS = {
    # JavaScript variations
    'js': 'javascript',
    'javascript': 'javascript',
    'java-script': 'javascript',
    'ecmascript': 'javascript',
    
    # TypeScript
    'ts': 'typescript',
    'typescript': 'typescript',
    
    # Python
    'python': 'python',
    'python3': 'python',
    'py': 'python',
    
    # Databases
    'postgresql': 'postgresql',
    'postgres': 'postgresql',
    'psql': 'postgresql',
    'mysql': 'mysql',
    'mongodb': 'mongodb',
    'mongo': 'mongodb',
    'sql': 'sql',
    'nosql': 'nosql',
    'database': 'database',
    'db': 'database',
    
    # Frontend Frameworks
    'react': 'react',
    'reactjs': 'react',
    'react.js': 'react',
    'vue': 'vue',
    'vuejs': 'vue',
    'vue.js': 'vue',
    'angular': 'angular',
    'angularjs': 'angular',
    
    # Backend Frameworks
    'django': 'django',
    'flask': 'flask',
    'fastapi': 'fastapi',
    'express': 'express',
    'expressjs': 'express',
    'express.js': 'express',
    'nodejs': 'nodejs',
    'node': 'nodejs',
    'node.js': 'nodejs',
    
    # Cloud Platforms
    'aws': 'aws',
    'amazon': 'aws',
    'ec2': 'aws',
    's3': 'aws',
    'azure': 'azure',
    'gcp': 'gcp',
    'google cloud': 'gcp',
    'heroku': 'heroku',
    
    # DevOps & Tools
    'docker': 'docker',
    'kubernetes': 'kubernetes',
    'k8s': 'kubernetes',
    'git': 'git',
    'github': 'git',
    'gitlab': 'git',
    'ci': 'cicd',
    'cd': 'cicd',
    'cicd': 'cicd',
    'jenkins': 'jenkins',
    
    # APIs
    'api': 'api',
    'apis': 'api',
    'rest': 'rest',
    'restful': 'rest',
    'graphql': 'graphql',
    
    # Testing
    'testing': 'testing',
    'test': 'testing',
    'tdd': 'testing',
    'unit test': 'testing',
    'pytest': 'testing',
    'jest': 'testing',
    
    # Common terms
    'agile': 'agile',
    'scrum': 'agile',
    'frontend': 'frontend',
    'front-end': 'frontend',
    'backend': 'backend',
    'back-end': 'backend',
    'fullstack': 'fullstack',
    'full-stack': 'fullstack',
    'full stack': 'fullstack',
}


def normalize_skill(token):
    """
    Normalize a skill token to its canonical form.
    
    Args:
        token: Single word token (lowercase)
        
    Returns:
        Normalized skill name, or original token if no mapping exists
    """
    return SKILL_SYNONYMS.get(token, token)


def normalize_tokens(tokens):
    """
    Normalize a list of tokens using skill synonyms.
    
    Args:
        tokens: List of word tokens
        
    Returns:
        List of normalized tokens
    """
    return [normalize_skill(token) for token in tokens]


# ============================================================================
# ENHANCEMENT #3: WEIGHTED SCORING
# ============================================================================

# High priority technical skills (3x weight)
HIGH_PRIORITY_SKILLS = {
    'python', 'javascript', 'typescript', 'java', 'c++', 'cpp', 'csharp', 'c#',
    'ruby', 'php', 'go', 'golang', 'rust', 'swift', 'kotlin', 'scala',
    'django', 'flask', 'fastapi', 'react', 'vue', 'angular', 'nodejs',
    'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes',
    'machine learning', 'ml', 'ai', 'deep learning', 'data science',
}

# Medium priority tools/platforms (2x weight)
MEDIUM_PRIORITY_SKILLS = {
    'git', 'jenkins', 'cicd', 'agile', 'scrum',
    'rest', 'api', 'graphql', 'microservices',
    'testing', 'tdd', 'unit', 'integration',
    'linux', 'unix', 'windows', 'macos',
    'html', 'css', 'sass', 'bootstrap', 'tailwind',
    'sql', 'nosql', 'database',
    'frontend', 'backend', 'fullstack',
}

# Low priority general terms (1x weight) - everything else


def get_skill_weight(token):
    """
    Get the importance weight for a skill/keyword.
    
    Args:
        token: Normalized skill token
        
    Returns:
        Weight multiplier (3, 2, or 1)
    """
    if token in HIGH_PRIORITY_SKILLS:
        return 3
    elif token in MEDIUM_PRIORITY_SKILLS:
        return 2
    else:
        return 1


def weighted_score_resume(resume_text, job_description):
    """
    Calculate weighted resume match score.
    Skills are weighted by importance: High (3x), Medium (2x), Low (1x)
    
    Args:
        resume_text: Full text of the resume
        job_description: Job posting description text
        
    Returns:
        tuple: (score, matched_keywords, missing_keywords, details)
    """
    # Tokenize, filter, and normalize
    job_tokens = normalize_tokens(tokenize_and_filter(job_description))
    resume_tokens = normalize_tokens(tokenize_and_filter(resume_text))
    
    job_tokens_set = set(job_tokens)
    resume_tokens_set = set(resume_tokens)
    
    # Calculate matches
    matched = job_tokens_set & resume_tokens_set
    missing = job_tokens_set - resume_tokens_set
    
    if not job_tokens_set:
        return 0, [], [], {}
    
    # Calculate weighted score
    total_weight = sum(get_skill_weight(token) for token in job_tokens_set)
    matched_weight = sum(get_skill_weight(token) for token in matched)
    
    score = int(100 * matched_weight / total_weight) if total_weight > 0 else 0
    
    # Prepare detailed breakdown
    details = {
        'total_keywords': len(job_tokens_set),
        'matched_count': len(matched),
        'missing_count': len(missing),
        'total_weight': total_weight,
        'matched_weight': matched_weight,
        'weighted_score': score,
    }
    
    return score, sorted(list(matched)), sorted(list(missing)), details


# ============================================================================
# ENHANCEMENT #4: FUZZY MATCHING
# ============================================================================

def calculate_similarity(word1, word2):
    """
    Calculate similarity ratio between two words.
    
    Args:
        word1, word2: Words to compare
        
    Returns:
        Similarity ratio (0.0 to 1.0)
    """
    return SequenceMatcher(None, word1, word2).ratio()


def find_fuzzy_matches(job_tokens, resume_tokens, threshold=0.85):
    """
    Find fuzzy matches between job and resume tokens.
    
    Args:
        job_tokens: Set of job requirement tokens
        resume_tokens: Set of resume tokens
        threshold: Minimum similarity ratio (0.85 = 85% similar)
        
    Returns:
        dict: Mapping of job tokens to their fuzzy matched resume tokens
    """
    fuzzy_matches = {}
    
    for job_token in job_tokens:
        if job_token in resume_tokens:
            # Exact match, skip fuzzy
            continue
            
        best_match = None
        best_score = 0
        
        for resume_token in resume_tokens:
            similarity = calculate_similarity(job_token, resume_token)
            if similarity >= threshold and similarity > best_score:
                best_match = resume_token
                best_score = similarity
        
        if best_match:
            fuzzy_matches[job_token] = {
                'matched_to': best_match,
                'similarity': round(best_score, 2)
            }
    
    return fuzzy_matches


def fuzzy_score_resume(resume_text, job_description, fuzzy_threshold=0.85):
    """
    Calculate weighted resume score with fuzzy matching support.
    Allows partial credit for similar words (e.g., "developer" ~ "development")
    
    Args:
        resume_text: Full text of the resume
        job_description: Job posting description text
        fuzzy_threshold: Minimum similarity for fuzzy match (default 0.85 = 85%)
        
    Returns:
        tuple: (score, matched_keywords, missing_keywords, fuzzy_matches, details)
    """
    # Tokenize, filter, and normalize
    job_tokens = normalize_tokens(tokenize_and_filter(job_description))
    resume_tokens = normalize_tokens(tokenize_and_filter(resume_text))
    
    job_tokens_set = set(job_tokens)
    resume_tokens_set = set(resume_tokens)
    
    # Find exact matches
    exact_matched = job_tokens_set & resume_tokens_set
    missing = job_tokens_set - exact_matched
    
    # Find fuzzy matches for missing keywords
    fuzzy_matches = find_fuzzy_matches(missing, resume_tokens_set, fuzzy_threshold)
    
    # Calculate weighted score
    total_weight = 0
    matched_weight = 0
    
    for token in job_tokens_set:
        weight = get_skill_weight(token)
        total_weight += weight
        
        if token in exact_matched:
            # Full credit for exact match
            matched_weight += weight
        elif token in fuzzy_matches:
            # Partial credit for fuzzy match (similarity * weight)
            similarity = fuzzy_matches[token]['similarity']
            matched_weight += weight * similarity
    
    score = int(100 * matched_weight / total_weight) if total_weight > 0 else 0
    
    # Update missing to only include items without fuzzy match
    truly_missing = [token for token in missing if token not in fuzzy_matches]
    
    # Prepare detailed breakdown
    details = {
        'total_keywords': len(job_tokens_set),
        'exact_matches': len(exact_matched),
        'fuzzy_matches': len(fuzzy_matches),
        'missing_count': len(truly_missing),
        'total_weight': total_weight,
        'matched_weight': round(matched_weight, 2),
        'weighted_score': score,
    }
    
    return score, sorted(list(exact_matched)), sorted(truly_missing), fuzzy_matches, details


# ============================================================================
# ENHANCEMENT #5: AI SEMANTIC MATCHING
# ============================================================================

def ai_semantic_match(resume_text, job_description, candidate_name="Candidate"):
    """
    Use AI to perform deep semantic analysis of candidate-job fit.
    Evaluates beyond keywords to understand context, transferable skills, etc.
    
    Args:
        resume_text: Full text of the resume
        job_description: Job posting description text
        candidate_name: Name of candidate for personalized analysis
        
    Returns:
        dict: {
            'technical_skills_score': 0-100,
            'experience_level_score': 0-100,
            'overall_score': 0-100,
            'grade': 'A'/'B'/'C'/'D'/'F',
            'reasoning': str,
            'strengths': list,
            'concerns': list,
            'recommendation': str
        }
    """
    # Truncate texts to fit in prompt
    resume_snippet = resume_text[:8000] if resume_text else "No resume text available"
    job_snippet = job_description[:4000] if job_description else "No job description"
    
    prompt = f"""You are an expert technical recruiter evaluating candidate-job fit.

JOB DESCRIPTION:
{job_snippet}

CANDIDATE RESUME:
{resume_snippet}

Evaluate this candidate for the job on multiple dimensions. Provide your response as valid JSON with these exact fields:

{{
  "technical_skills_score": <0-100 number>,
  "experience_level_score": <0-100 number>,
  "overall_score": <0-100 number>,
  "grade": "<A/B/C/D/F letter grade>",
  "reasoning": "<2-3 sentence explanation of the overall match>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "concerns": ["<concern 1>", "<concern 2>"],
  "recommendation": "<Recommend/Consider/Not Recommended>"
}}

Consider:
- Direct skill matches and transferable skills
- Experience level vs requirements
- Domain expertise and relevant background
- Overall cultural and technical fit

Be fair but honest. Similar technologies should count (e.g., Flask experience helps with Django).
"""

    try:
        # Use OpenRouter with DeepSeek R1 T2 Chimera (FREE version - advanced reasoning)
        response = client.chat.completions.create(
            model='tngtech/deepseek-r1t2-chimera:free',  # DeepSeek R1 reasoning model (FREE)
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=800,
            temperature=0.3,
            timeout=40,  # 40 second timeout for this specific call
            extra_headers={
                "HTTP-Referer": settings.OPENROUTER_APP_NAME,
                "X-Title": settings.OPENROUTER_APP_NAME,
            }
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Try to parse JSON response
        # Sometimes AI wraps JSON in markdown code blocks
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        result = json.loads(response_text)
        
        # Validate required fields
        required_fields = ['technical_skills_score', 'experience_level_score', 
                          'overall_score', 'grade', 'reasoning', 'strengths', 
                          'concerns', 'recommendation']
        
        for field in required_fields:
            if field not in result:
                result[field] = get_default_value(field)
        
        return result
        
    except Exception as e:
        # Return default structure if AI call fails
        error_type = type(e).__name__
        error_msg = str(e)
        
        # Log the error for debugging
        print(f"AI semantic match error ({error_type}): {error_msg}")
        
        # Provide user-friendly error message
        if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
            reasoning = 'AI analysis timed out (server busy). Keyword scoring still available.'
        elif 'api' in error_msg.lower() or 'key' in error_msg.lower():
            reasoning = 'AI API unavailable. Please check API key configuration.'
        else:
            reasoning = 'AI analysis unavailable. Using keyword scoring only.'
        
        return {
            'technical_skills_score': 0,
            'experience_level_score': 0,
            'overall_score': 0,
            'grade': 'N/A',
            'reasoning': reasoning,
            'strengths': [],
            'concerns': ['AI analysis unavailable - manual review recommended'],
            'recommendation': 'Manual review required',
            'error': f'{error_type}: {error_msg[:100]}'  # Truncate long errors
        }


def get_default_value(field):
    """Helper to get default value for missing AI response fields"""
    if field in ['technical_skills_score', 'experience_level_score', 'overall_score']:
        return 0
    elif field == 'grade':
        return 'N/A'
    elif field == 'reasoning':
        return 'Analysis incomplete'
    elif field in ['strengths', 'concerns']:
        return []
    elif field == 'recommendation':
        return 'Manual review required'
    return None


# ============================================================================
# UNIFIED SCORING FUNCTION (Combines all enhancements)
# ============================================================================

def advanced_score_resume(resume_text, job_description, candidate_name="Candidate", 
                         use_ai=True, fuzzy_threshold=0.85):
    """
    Perform complete advanced scoring with all enhancements.
    Returns both keyword-based and AI-based scores.
    
    Args:
        resume_text: Full text of the resume
        job_description: Job posting description text
        candidate_name: Name for personalized AI analysis
        use_ai: Whether to include AI semantic analysis (slower)
        fuzzy_threshold: Similarity threshold for fuzzy matching
        
    Returns:
        dict: Complete scoring results with all metrics
    """
    # Phase 1: Enhanced keyword scoring (fast)
    keyword_score, exact_matches, missing, fuzzy_matches, details = fuzzy_score_resume(
        resume_text, job_description, fuzzy_threshold
    )
    
    result = {
        'keyword_score': keyword_score,
        'exact_matches': exact_matches,
        'fuzzy_matches': fuzzy_matches,
        'missing_keywords': missing,
        'scoring_details': details,
    }
    
    # Phase 2: AI semantic analysis (slower, optional)
    if use_ai and settings.OPENROUTER_API_KEY:
        ai_result = ai_semantic_match(resume_text, job_description, candidate_name)
        result['ai_analysis'] = ai_result
        result['ai_score'] = ai_result.get('overall_score', 0)
        result['ai_grade'] = ai_result.get('grade', 'N/A')
    else:
        result['ai_analysis'] = None
        result['ai_score'] = None
        result['ai_grade'] = None
    
    return result


# ============================================================================
# BASIC SCORING (with stop words filtering)
# ============================================================================

def basic_score_resume(resume_text, job_description):
    """
    Calculate resume match score with stop words filtering and normalization.
    
    Args:
        resume_text: Full text of the resume
        job_description: Job posting description text
        
    Returns:
        tuple: (score, matched_keywords, missing_keywords)
    """
    # Tokenize, filter stop words, and normalize both texts
    job_tokens = normalize_tokens(tokenize_and_filter(job_description))
    resume_tokens = normalize_tokens(tokenize_and_filter(resume_text))
    
    job_tokens = set(job_tokens)
    resume_tokens = set(resume_tokens)
    
    # Calculate matches
    matched = job_tokens & resume_tokens
    missing = job_tokens - resume_tokens
    
    if not job_tokens:
        return 0, [], []
    
    # Calculate score
    score = int(100 * len(matched) / len(job_tokens))
    
    return score, sorted(list(matched)), sorted(list(missing))

