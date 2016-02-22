from datetime import date

from django.core import mail
from django.test import TestCase

from feedback.tests.factories import SubjectFactory
from feedback.feedbacks_scheduler import FeedbackSchedulerReport
from .send_reports import send

class EmailTest(TestCase):
    def setUp(self):
        self.subject = SubjectFactory()
        self.reports = [FeedbackSchedulerReport("Histoire de l'economie", False, date(year=2016, month=10, day=2)),
                        FeedbackSchedulerReport("Histoire de France", True, date(year=2016, month=11, day=2))]

    def test_send_email(self):
        send(self.reports)
        self.assertEqual(len(mail.outbox), 1)
