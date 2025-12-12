from django.db import models
from django.contrib.postgres.search import SearchVectorField


class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    required_skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class Candidate(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("shortlisted", "Shortlisted"),
        ("interview", "Interview"),
        ("hired", "Hired"),
        ("rejected", "Rejected"),
    ]
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='candidates', null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    skills = models.JSONField(default=list, blank=True)
    experience_years = models.FloatField(default=0)
    education = models.TextField(blank=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_text = models.TextField(blank=True)
    
    # Legacy scoring (kept for backward compatibility)
    score = models.FloatField(default=0)
    matched_keywords = models.TextField(blank=True)
    missing_keywords = models.TextField(blank=True)
    
    # Advanced scoring fields
    keyword_score = models.FloatField(default=0, help_text='Enhanced keyword-based score (0-100)')
    ai_score = models.FloatField(default=0, null=True, blank=True, help_text='AI semantic match score (0-100)')
    ai_grade = models.CharField(max_length=5, blank=True, help_text='AI match grade (A-F)')
    ai_reasoning = models.TextField(blank=True, help_text='AI analysis reasoning')
    fuzzy_matches = models.JSONField(default=dict, blank=True, help_text='Fuzzy matched keywords')
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("shortlisted", "Shortlisted"),
        ("interview", "Interview"),
        ("hired", "Hired"),
        ("rejected", "Rejected"),
    ]
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    resume_file = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.candidate} -> {self.job}"