from collections import namedtuple
from datetime import datetime, timedelta
import datetime as datetime_module

from django.conf import settings
from pytz import timezone

from feedback.utils import next_monday_date, current_time
from feedback.models import Feedback, get_feedback_class

FeedbackSchedulerReport = namedtuple('FeedbackSchedulerReport', ['subject', 'done', 'next_feedback_date'])

class FeedbackScheduler(object):
    """Schedule weekly feedbacks taking into account the forgetting curve.

    We have one week to do the feedback. It starts on monday until
    sunday at 11:42pm.

    Args:
        subject (models.Subject): The feedback subject.
    """

    def __init__(self, subject):
        self.subject = subject
        self.last_feedback = self.subject.get_last_feedback()
        self.nbr_of_feedbacks = Feedback.objects.filter(subject=subject).count()

    def schedule(self):
        """Schedule next feedback session based on previous feedbacks

        Return: A tuple ()
        """
        is_last_feedback_done = self.last_feedback.done
        if is_last_feedback_done: ## Nice , create a new feedback session.
            next_feedback_date = self.calculate_next_feedback_date()
            self.subject.update_feedback_session_duration()
            self.subject.update_penalties(is_feedback_done=True)

            get_feedback_class()(subject=self.subject, date=next_feedback_date).save()

        elif not is_last_feedback_done and self.is_feedback_time_elapsed(): ## Not good, postpone the feedback to next monday, add penalties.
            self.last_feedback.date = next_monday_date()
            self.subject.update_penalties(is_feedback_done=False)
            self.last_feedback.save()

        return FeedbackSchedulerReport(subject=self.subject.title,
                                       done=is_last_feedback_done,
                                       next_feedback_date=self.subject.get_last_feedback().date)
        ## Here We still have time to do the feedback, don't do anything.

    def is_feedback_time_elapsed(self):
        limite_date = datetime.combine(self.last_feedback.date,
                                       datetime_module.time(0)) + timedelta(weeks=1, minutes=-18)
        if timezone(settings.CURRENT_TIME_ZONE).localize(limite_date) < current_time():
            return True
        return False

    def calculate_next_feedback_date(self):
        next_feedback_date = next_monday_date() + timedelta(weeks=self.nbr_of_feedbacks - self.subject.penalties)
        if next_feedback_date < next_monday_date():
            next_feedback_date = next_monday_date()
        return next_feedback_date
