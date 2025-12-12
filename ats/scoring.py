import re

def tokenize(text):
    return re.findall(r'\w+', text.lower())

def score_resume(resume_text, job_description):
    job_tokens = set(tokenize(job_description))
    resume_tokens = set(tokenize(resume_text))
    matched = job_tokens & resume_tokens
    missing = job_tokens - resume_tokens
    if not job_tokens:
        return 0, [], []
    score = int(100 * len(matched) / len(job_tokens))
    return score, list(matched), list(missing)
