from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import JobPost, Candidate, Application
from .forms import JobCreateForm, CandidateUploadForm
from .parsers import parse_resume
from .scoring import score_resume
from .advanced_scoring import advanced_score_resume
from django.db.models import Count, Q

class DashboardView(LoginRequiredMixin, TemplateView):
	template_name = 'dashboard.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['total_jobs'] = JobPost.objects.count()
		context['total_candidates'] = Candidate.objects.count()
		context['shortlisted'] = Application.objects.filter(status='shortlisted').count()
		context['rejected'] = Application.objects.filter(status='rejected').count()
		context['recent_jobs'] = JobPost.objects.annotate(num_applications=Count('applications')).order_by('-created_at')[:5]
		return context

class JobListView(LoginRequiredMixin, ListView):
	model = JobPost
	template_name = 'jobs/list.html'
	context_object_name = 'jobs'
	ordering = ['-created_at']

class JobCreateView(LoginRequiredMixin, CreateView):
	model = JobPost
	form_class = JobCreateForm
	template_name = 'jobs/create.html'
	success_url = reverse_lazy('job_list')

	def form_valid(self, form):
		# Handle required_skills from the multi-select
		import json
		skills_json = self.request.POST.get('required_skills', '[]')
		try:
			form.instance.required_skills = json.loads(skills_json)
		except:
			form.instance.required_skills = []
		
		messages.success(self.request, f'Job "{form.instance.title}" created successfully!')
		return super().form_valid(form)

class JobDetailView(LoginRequiredMixin, DetailView):
	model = JobPost
	template_name = 'jobs/detail.html'
	context_object_name = 'job'

class CandidateListView(LoginRequiredMixin, ListView):
	model = Candidate
	template_name = 'candidates/list.html'
	context_object_name = 'candidates'
	paginate_by = 20

	def get_queryset(self):
		qs = super().get_queryset().select_related('job')
		search = self.request.GET.get('search', '')
		status = self.request.GET.get('status', '')
		order_by = self.request.GET.get('order_by', '-created_at')
		if search:
			qs = qs.filter(Q(name__icontains=search) | Q(email__icontains=search))
		if status:
			qs = qs.filter(status=status)
		if order_by:
			qs = qs.order_by(order_by)
		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['status_choices'] = Candidate.STATUS_CHOICES
		return context

class CandidateUploadView(LoginRequiredMixin, CreateView):
	model = Candidate
	form_class = CandidateUploadForm
	template_name = 'candidates/upload.html'

	def get_initial(self):
		initial = super().get_initial()
		job_id = self.request.GET.get('job')
		if job_id:
			initial['job'] = job_id
		return initial

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['jobs'] = JobPost.objects.all()
		return context

	def form_valid(self, form):
		# Parse the uploaded resume file
		if 'resume_file' in self.request.FILES:
			file = self.request.FILES['resume_file']
			filename = file.name
			job = form.cleaned_data['job']
			
			print(f"📄 Processing resume: {filename} for job: {job.title}")
			
			try:
				# Parse resume with AI
				parsed = parse_resume(file, filename, None)
				form.instance.resume_text = parsed.get('text', '')
				
				print(f"✅ Resume text extracted: {len(form.instance.resume_text)} characters")
				
				# Use parsed data if available, otherwise use form data
				if not form.instance.email and parsed.get('email'):
					form.instance.email = parsed['email']
				if not form.instance.phone and parsed.get('phone'):
					form.instance.phone = parsed['phone']
				
				# Update skills and experience if available
				if parsed.get('skills'):
					form.instance.skills = parsed['skills']
					print(f"✅ Skills extracted: {parsed['skills']}")
				if parsed.get('experience'):
					form.instance.experience_years = parsed['experience']
					print(f"✅ Experience: {parsed['experience']} years")
				if parsed.get('education'):
					form.instance.education = parsed['education']
				
			except Exception as e:
				print(f"❌ Resume parsing error: {e}")
				import traceback
				traceback.print_exc()
				messages.error(self.request, f'Resume parsing failed: {str(e)}')
				form.instance.resume_text = "Error parsing resume"
			
			# Only proceed with scoring if we have resume text
			if form.instance.resume_text and form.instance.resume_text != "Error parsing resume":
				try:
					# Build scoring context from description AND required skills
					scoring_text = job.description
					if job.required_skills:
						# Add required skills to scoring context
						skills_text = " ".join(job.required_skills) if isinstance(job.required_skills, list) else str(job.required_skills)
						scoring_text = f"{scoring_text}\n\nRequired Skills: {skills_text}"
					
					if not scoring_text.strip():
						scoring_text = "General candidate evaluation"  # Fallback
					
					print(f"📊 Scoring Context Length: {len(scoring_text)} chars")
					
					# Legacy scoring (backward compatibility)
					score, matched, missing = score_resume(form.instance.resume_text, scoring_text)
					form.instance.score = score
					form.instance.matched_keywords = ", ".join(matched[:50])
					form.instance.missing_keywords = ", ".join(missing[:50])
					
					print(f"✅ Legacy score: {score}%")
					
					# Advanced scoring with all enhancements
					advanced_results = advanced_score_resume(
						form.instance.resume_text,
						scoring_text,
						candidate_name=form.instance.name,
						use_ai=True
					)
					
					# Store enhanced keyword score
					form.instance.keyword_score = advanced_results.get('keyword_score', 0)
					print(f"✅ Keyword score: {form.instance.keyword_score}%")
					
					# Store fuzzy matches
					form.instance.fuzzy_matches = advanced_results.get('fuzzy_matches', {})
					
					# Store AI analysis results
					ai_analysis = advanced_results.get('ai_analysis', {})
					if ai_analysis and 'error' not in ai_analysis:
						form.instance.ai_score = ai_analysis.get('overall_score', 0)
						form.instance.ai_grade = ai_analysis.get('grade', '')
						
						print(f"✅ AI Score: {form.instance.ai_score}%, Grade: {form.instance.ai_grade}")
						
						# Create readable reasoning summary
						reasoning_parts = []
						if ai_analysis.get('reasoning'):
							reasoning_parts.append(ai_analysis['reasoning'])
						if ai_analysis.get('strengths'):
							reasoning_parts.append(f"Strengths: {', '.join(ai_analysis['strengths'][:3])}")
						if ai_analysis.get('concerns'):
							reasoning_parts.append(f"Concerns: {', '.join(ai_analysis['concerns'][:3])}")
						if ai_analysis.get('recommendation'):
							reasoning_parts.append(f"Recommendation: {ai_analysis['recommendation']}")
						
						form.instance.ai_reasoning = " | ".join(reasoning_parts)
						
						messages.success(
							self.request,
							f'✅ Candidate uploaded! Keyword Score: {form.instance.keyword_score}% | AI Grade: {form.instance.ai_grade}'
						)
					else:
						# AI analysis failed but keyword score worked
						error_msg = ai_analysis.get('error', 'Unknown error') if ai_analysis else 'No AI analysis returned'
						print(f"⚠️ AI analysis failed: {error_msg}")
						messages.warning(
							self.request,
							f'Candidate uploaded with keyword score ({form.instance.keyword_score}%). AI analysis failed: {error_msg}'
						)
					
				except Exception as e:
					# Fallback to basic scoring if advanced fails
					print(f"❌ Advanced scoring error: {e}")
					import traceback
					traceback.print_exc()
					messages.error(
						self.request,
						f'Scoring failed: {str(e)}. Candidate saved but without scores.'
					)
			else:
				messages.error(
					self.request,
					'Failed to extract text from resume. Please check the PDF file.'
				)
		else:
			messages.error(self.request, 'No resume file uploaded.')
		
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('job_detail', args=[self.object.job.pk])

class CandidateDetailView(LoginRequiredMixin, DetailView):
	model = Candidate
	template_name = 'candidates/detail.html'
	context_object_name = 'candidate'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['status_choices'] = Candidate.STATUS_CHOICES
		return context

class CandidateStatusUpdateView(LoginRequiredMixin, View):
	def post(self, request, pk):
		candidate = get_object_or_404(Candidate, pk=pk)
		status = request.POST.get('status')
		if status in dict(Candidate.STATUS_CHOICES):
			candidate.status = status
			candidate.save()
			messages.success(request, 'Status updated.')
		return redirect('candidate_detail', pk=pk)