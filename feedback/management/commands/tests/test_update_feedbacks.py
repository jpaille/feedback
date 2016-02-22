from django.core.management import call_command
from django.test import TestCase, override_settings

from feedback.tests.factories import SubjectFactory
from feedback.models import Feedback
from feedback.utils import previous_monday_date
class UpdateFeedbacksTestCase(TestCase):
    """" Test update_feedbacks command."""
    def setUp(self):
        self.subject = SubjectFactory()

    @override_settings(USE_GOOGLE_CALENDAR=False)
    def test_update_feedbacks_with_google_calendar(self):
        feedback = self.subject.get_last_feedback()
        feedback._done = True
        feedback.date = previous_monday_date()
        feedback.save()
        call_command('update_feedbacks')
        self.assertEqual(2, Feedback.objects.filter(subject=self.subject).count())
