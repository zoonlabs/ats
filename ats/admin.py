from django.contrib import admin
from .models import JobPost, Candidate, Application


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'score', 'created_at')
    search_fields = ('name', 'email')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'status', 'created_at')
    list_filter = ('status', 'job')