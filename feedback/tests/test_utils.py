from datetime import timedelta

from django.test import TestCase

from feedback.utils import get_hours_and_minutes_from_timedelta, Duration

class SubjectTestCase(TestCase):
    def test_get_hours_and_minutes_from_timedelta(self):
        self.assertEqual(Duration(3, 43), get_hours_and_minutes_from_timedelta(timedelta(seconds=13420)))
