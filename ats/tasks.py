from celery import shared_task
from .models import Application, Candidate
from .parsers import extract_text_from_file, parse_resume_with_openai
from .utils import compute_score
from django.core.files.storage import default_storage
import tempfile


@shared_task
def parse_and_score_application(application_id):
    app = Application.objects.get(pk=application_id)
    # download file if using remote storage
    path = app