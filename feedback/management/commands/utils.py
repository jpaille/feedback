from feedback.models import Feedback
from feedback.utils import previous_monday_date

def get_current_week_subjects():
    feedbacks = Feedback.objects.filter(date=previous_monday_date())
    return [fb.subject for fb in feedbacks]
