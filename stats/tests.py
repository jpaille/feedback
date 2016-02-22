from django.test import TestCase, override_settings

from stats.utils import get_feedback_progress, get_lost_info_percentage
from feedback.tests.factories import SubjectFactory, FeedbackFactory, get_feedback_factory_class

@override_settings(USE_GOOGLE_CALENDAR=False)
class UtilsTestCase(TestCase):
    def setUp(self):
        self.subject = SubjectFactory()
    def test_get_feedback_progress(self):
        self.assertEqual(get_feedback_progress(get_feedback_factory_class().create_batch(5, subject=self.subject)),
                         50)
    def test_get_forgetting_percentage(self):
        self.assertEqual(0, get_lost_info_percentage(self.subject))
    def test_get_lost_info_percentage(self):
        get_feedback_factory_class().create_batch(3, subject=self.subject, _done=True)
        self.subject.penalties = 2
        self.assertEqual(33.3, get_lost_info_percentage(self.subject))

@override_settings(USE_GOOGLE_CALENDAR=True)
class UtilsTestCaseWithGoogleCalendar(UtilsTestCase):
    pass
