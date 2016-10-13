from datetime import timedelta

from django.template import Template, Context
from django.test import TestCase

class TestTimedeltaTemplateTag(TestCase):

    TEMPLATE = Template("{%load timedelta%}{{ timedelta_object|timedelta}}")

    def test_timedelta(self):
        rendered = self.TEMPLATE.render(Context({'timedelta_object':timedelta(hours=2, minutes=30)}))
        self.assertEqual('2h30', rendered)
    def test_timedelta_with_no_minutes(self):
        rendered = self.TEMPLATE.render(Context({'timedelta_object':timedelta(hours=3)}))
        self.assertEqual('3h', rendered)
    def test_timedelta_with_no_hours(self):
        rendered = self.TEMPLATE.render(Context({'timedelta_object':timedelta(minutes=30)}))
        self.assertEqual('30mins', rendered)
    def test_timedelta_with_three_minutes(self):
        rendered = self.TEMPLATE.render(Context({'timedelta_object':timedelta(minutes=3)}))
        self.assertEqual('3mins', rendered)
    def test_timedelta_with_leading_zero_in_minutes(self):
        rendered = self.TEMPLATE.render(Context({'timedelta_object':timedelta(hours=2, minutes=4)}))
        self.assertEqual('2h04', rendered)
