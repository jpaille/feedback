from django.core.management.base import BaseCommand
from django.conf import settings

from feedback.feedbacks_scheduler import FeedbackScheduler
from mail_reports.send_reports import send
from .utils import get_current_week_subjects

class Command(BaseCommand):
    help = 'Schedule feedbacks sessions.'

    def handle(self, *args, **options):
        subjects = get_current_week_subjects()
        feedback_scheduler_reports = []
        for subject in subjects:
            feedback_scheduler = FeedbackScheduler(subject)
            feedback_scheduler_reports.append(feedback_scheduler.schedule())
        if settings.USE_MAIL_REPORT_NOTIFICATION:
            send(feedback_scheduler_reports)
