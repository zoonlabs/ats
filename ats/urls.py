from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job_create'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('candidates/', views.CandidateListView.as_view(), name='candidate_list'),
    path('candidates/upload/', views.CandidateUploadView.as_view(), name='candidate_upload'),
    path('candidates/<int:pk>/', views.CandidateDetailView.as_view(), name='candidate_detail'),
    path('candidates/<int:pk>/status/', views.CandidateStatusUpdateView.as_view(), name='candidate_status_update'),
]
