import datetime

from django.core.management import call_command
from django.test import TestCase, override_settings

from feedback.tests.factories import SubjectFactory
from feedback.models import Feedback
from feedback.utils import previous_monday_date

@override_settings(USE_GOOGLE_CALENDAR=True)
class UpdateFeedbacksTestCase(TestCase):
    """" Test update_feedbacks command."""
    def setUp(self):
        self.subject = SubjectFactory()

    def test_update_feedbacks_with_google_calendar(self):
        feedback = self.subject.get_last_feedback()
        self.assertEqual(feedback.duration, datetime.timedelta(hours=2))
        feedback.google_calendar_client.update_event(feedback.event_id,
                                                     fields={'location' : '01:00',
                                                             'description' : 'd'})
        feedback.date = previous_monday_date()
        feedback.save()
        call_command('update_feedbacks')
        self.assertEqual(2, Feedback.objects.filter(subject=self.subject).count())
        last_feedback = self.subject.get_last_feedback()
        self.assertEqual(last_feedback.duration, datetime.timedelta(hours=1))
        self.assertEqual(last_feedback.google_calendar_client.get_event(last_feedback.event_id)['location'],
                         '1:00')
