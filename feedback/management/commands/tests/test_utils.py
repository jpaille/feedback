from django.test import TestCase, override_settings

from feedback.tests.factories import get_feedback_factory_class, SubjectFactory
from feedback.utils import previous_monday_date, next_monday_date
from feedback.management.commands.utils import get_current_week_subjects

@override_settings(USE_GOOGLE_CALENDAR=False)
class UtilTestCase(TestCase):
    def test_get_current_week_subjects(self):
        current_week_subject = SubjectFactory(title='current_week_subject')
        next_week_subject = SubjectFactory(title='next_week_subject')
        get_feedback_factory_class()(date=previous_monday_date(), subject=current_week_subject)
        get_feedback_factory_class()(date=next_monday_date(), subject=next_week_subject)
        self.assertEqual([current_week_subject], get_current_week_subjects())

@override_settings(USE_GOOGLE_CALENDAR=True)
class UtilTestCaseWithGoogleCalendar(UtilTestCase):
    pass
