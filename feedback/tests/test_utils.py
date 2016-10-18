from django.test import TestCase
from feedback.utils import get_google_calendar_event_color_from_penalties

class UtilsTestCase(TestCase):
    def test_get_google_calendar_event_color_from_penalties(self):
        self.assertEqual('11', get_google_calendar_event_color_from_penalties(10))
