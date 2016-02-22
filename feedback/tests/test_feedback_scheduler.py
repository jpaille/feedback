from datetime import datetime
from  datetime import timedelta
import datetime as datetime_module
from mock import patch

from django.test import TestCase, override_settings
from pytz import utc

from feedback.feedbacks_scheduler import FeedbackScheduler, FeedbackSchedulerReport
from feedback.models import Subject
from feedback.tests.factories import SubjectFactory, get_feedback_factory_class
from feedback.utils import next_monday_date, previous_monday_date

@override_settings(USE_GOOGLE_CALENDAR=False)
class FeedbackSchedulerTestCase(TestCase):
    def setUp(self):
        self.subject = SubjectFactory()
        self.feedback_class = get_feedback_factory_class()
    def test_nbr_of_feedbacks(self):
        self.feedback_class.create_batch(5, subject=self.subject)
        self.assertEqual(FeedbackScheduler(self.subject).nbr_of_feedbacks, 6)
    def test_schedule_first_feedback(self):
        self.assertEqual(FeedbackScheduler(self.subject).nbr_of_feedbacks, 1)
    def test_schedule_first_feedback_date(self):
        self.assertEqual(self.subject.get_last_feedback().date, next_monday_date())
    def test_schedule_feedback_done(self):
        feedback = self.feedback_class.create(subject=self.subject)
        feedback.done = True
        feedback.save()
        self.assertEqual(FeedbackScheduler(self.subject).nbr_of_feedbacks, 2)
        self.assertEqual(Subject.objects.get(title=self.subject.title).penalties, 0)
    def test_schedule_feedback_done_with_penalties(self):
        self.subject.penalties = 2
        self.subject.save()
        self.feedback_class.create_batch(3, subject=self.subject)
        self.feedback_class.create(subject=self.subject, _done=True)
        FeedbackScheduler(self.subject).schedule()
        last_feedback = self.subject.get_last_feedback()
        self.assertEqual(last_feedback.date, next_monday_date() + timedelta(weeks=3))
        self.assertEqual(Subject.objects.get(title=self.subject.title).penalties, 0)
    def test_schedule_feedback_time_elapsed(self):
        previous_monday = previous_monday_date()
        next_monday = next_monday_date()
        self.feedback_class(subject=self.subject, date=previous_monday)
        fake_datetime = datetime.combine(next_monday, datetime_module.time(0)) - timedelta(minutes=17) ## next sunday 11:43pm.
        with patch("feedback.feedbacks_scheduler.current_time", return_value=utc.localize(fake_datetime)):
            report_scheduler = FeedbackScheduler(self.subject).schedule()
        postponed_feedback = self.subject.get_last_feedback()
        self.assertEqual(postponed_feedback.date, next_monday)
        self.assertEqual(self.subject.penalties, 2)
        self.assertEqual(FeedbackSchedulerReport(self.subject.title, False, next_monday),
                         report_scheduler)

@override_settings(USE_GOOGLE_CALENDAR=True)
class FeedbackSchedulerTestCaseUsingGoogleCalendar(FeedbackSchedulerTestCase):
    pass
