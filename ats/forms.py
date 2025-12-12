from django import forms
from .models import JobPost, Candidate, Application


class JobCreateForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'required_skills']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CandidateUploadForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['job', 'name', 'email', 'phone', 'resume_file']
        widgets = {
            'job': forms.Select(attrs={'class': 'form-control'}),
        }