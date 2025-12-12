def compute_score(job: 'JobPost', parsed: dict) -> float:
    # deterministic scoring
    required = [s.lower() for s in (job.required_skills or [])]
    cand_skills = [s.lower() for s in parsed.get('skills', [])]
    if required:
        skill_match = len(set(required) & set(cand_skills)) / len(required)
    else:
        skill_match = 1.0
    skill_score = skill_match * 60
    exp = parsed.get('total_experience_years', 0) or 0
    req_years = 3
    exp_score = min(20, (exp / max(1, req_years)) * 20)
    edu_score = 0
    for ed in parsed.get('education', []):
        edl = ed.lower()
        if 'master' in edl:
            edu_score = 10
            break
        if 'bachelor' in edl:
            edu_score = max(edu_score, 7)
    total = skill_score + exp_score + edu_score
    return round(min(100, total), 2)