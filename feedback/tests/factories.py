import factory
from factory.django import DjangoModelFactory
from django.conf import settings

from feedback.models import Feedback, GoogleCalendarFeedback, Subject


class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject

    title = factory.Sequence(lambda n: 'Subject-%d' % n)
    nbr_of_cards = 15

class FeedbackFactory(DjangoModelFactory):
    class Meta:
        model = Feedback

class GoogleCalendarFeedbackFactory(DjangoModelFactory):
    class Meta:
        model = GoogleCalendarFeedback


def get_feedback_factory_class():
    if settings.USE_GOOGLE_CALENDAR:
        return GoogleCalendarFeedbackFactory
    return FeedbackFactory
