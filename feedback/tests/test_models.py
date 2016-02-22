from datetime import date, timedelta

from django.test import TestCase, override_settings

from feedback.tests.factories import SubjectFactory, get_feedback_factory_class
from feedback.models import Feedback

@override_settings(USE_GOOGLE_CALENDAR=False)
class SubjectTestCase(TestCase):
    def setUp(self):
        self.subject = SubjectFactory()
        self.feedback = self.subject.get_last_feedback()
    def test_save_subject(self):
        self.assertTrue(isinstance(Feedback.objects.get(subject=self.subject), Feedback))
    def test_get_last_feedback(self):
        self.assertEqual(Feedback.objects.get(subject=self.subject), self.feedback)
    def test_update_feedback_session_duration(self):
        self.assertEqual(self.feedback.duration, timedelta(seconds=7200))
        get_feedback_factory_class()(subject=self.subject, duration=timedelta(hours=4))
        self.subject.update_feedback_session_duration()
        self.assertEqual(self.subject.get_last_feedback().duration, timedelta(hours=4))
    def test_update_penalties_no_penalties_feedback_done(self):
        self.subject.update_penalties(True)
        self.assertEqual(self.subject.penalties, 0)
    def test_update_penalties_penalties_feedback_done(self):
        self.subject.penalties = 2
        self.subject.update_penalties(True)
        self.assertEqual(self.subject.penalties, 0)
    def test_update_penalties_penalties_feedback_not_done(self):
        self.subject.penalties = 2
        self.subject.update_penalties(False)
        self.assertEqual(self.subject.penalties, 4)

@override_settings(USE_GOOGLE_CALENDAR=True)
class SubjectTestCaseWithGoogleCalendar(SubjectTestCase):
    pass


class FeedbackTestCase():
    pass

@override_settings(USE_GOOGLE_CALENDAR=True)
class GoogleCalendarFeedbackTestCase(TestCase):
    def setUp(self):
        self.subject = SubjectFactory()
        self.feedback = self.subject.get_last_feedback()
    def test_save_feedback(self):
        self.assertTrue(self.feedback.google_calendar_client.get_event(self.feedback.event_id))
    def test_is_done(self):
        self.assertFalse(self.feedback.done)
        self.feedback.google_calendar_client.update_event(self.feedback.event_id, {"description" :"d"})
        self.assertTrue(self.feedback.done)
    def test_update_date(self):
        updated_date = date(2016, 9, 18)
        self.assertNotEqual(self.feedback.date, updated_date)
        self.feedback.date = updated_date
        self.feedback.save()
        event = self.feedback.google_calendar_client.get_event(self.feedback.event_id)
        self.assertEqual(event["start"]["date"], updated_date.strftime("%Y-%m-%d"))
        self.assertEqual(event["end"]["date"], updated_date.strftime("%Y-%m-%d"))
    def test_update_duration_field(self):
        self.assertEqual(self.feedback.duration, timedelta(seconds=7200))
        self.feedback.update_duration_field({"location" : "02:30"})
        self.assertEqual(self.feedback.duration, timedelta(hours=2, minutes=30))
    def test_delete_feedback(self):
        client = self.feedback.google_calendar_client
        event_id = self.feedback.event_id
        self.feedback.delete()
        self.assertEqual("cancelled", client.get_event(event_id)["status"])
