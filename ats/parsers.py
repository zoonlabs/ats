import os
import tempfile
from pdfminer.high_level import extract_text as pdf_extract
from openai import OpenAI
from django.conf import settings


# Initialize OpenRouter client with timeout
client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL,
    timeout=30.0,  # 30 second timeout for parsing
    max_retries=0,  # No retries to fail fast
)


def parse_resume(file_obj, filename=None, keywords=None):
    """
    Extracts text from a file-like object (PDF) and parses it with OpenAI.
    Returns a dict with parsed fields.
    """
    # Save file_obj to a temporary file for pdfminer
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename or 'resume.pdf')[1]) as tmp:
        tmp.write(file_obj.read())
        tmp_path = tmp.name
    text = extract_text_from_file(tmp_path)
    os.unlink(tmp_path)
    parsed = parse_resume_with_openai(text)
    parsed['text'] = text
    return parsed


def extract_text_from_file(path):
# currently handles PDFs (pdfminer)
    try:
        text = pdf_extract(path)
        if text and text.strip():
            return text
    except Exception:
        pass
    return ''


def parse_resume_with_openai(resume_text):
    import json
    if not resume_text:
        return {'email': None, 'phone': None, 'skills': [], 'experience': 0, 'education': ''}
    prompt = f"""
    You are a resume parser. Extract JSON with these fields: email (string or null), phone (string or null), skills (list of short lowercase strings), experience (number of years), education (string). Provide only valid JSON.
    Resume:\n""" + resume_text[:16000]
    try:
        # Use OpenRouter with DeepSeek R1 T2 Chimera (FREE version)
        response = client.chat.completions.create(
            model='tngtech/deepseek-r1t2-chimera:free',  # DeepSeek R1 reasoning model (FREE)
            messages=[{'role':'user','content':prompt}],
            max_tokens=500,
            temperature=0,
            timeout=25,  # 25 second timeout for parsing call
            extra_headers={
                "HTTP-Referer": settings.OPENROUTER_APP_NAME,
                "X-Title": settings.OPENROUTER_APP_NAME,
            }
        )
        text = response.choices[0].message.content
        # Parse the JSON response
        parsed = json.loads(text)
    except Exception as e:
        # Fallback: return default structure
        error_type = type(e).__name__
        print(f"Resume parsing error ({error_type}): {str(e)[:200]}")
        parsed = {'email': None, 'phone': None, 'skills': [], 'experience': 0, 'education': ''}
    return parsed