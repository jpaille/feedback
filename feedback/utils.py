from datetime import datetime, timedelta

from pytz import timezone as tz
from django.conf import settings
from django.utils import timezone

def next_monday_date():
    today = datetime.now().date()
    next_monday = today + timedelta(days=-today.weekday(), weeks=1)
    return next_monday

def previous_monday_date():
    return datetime.now().date() - timedelta(days=datetime.now().date().weekday())

def current_time():
    ## Activate the Europe time zone.
    timezone.activate(tz(settings.CURRENT_TIME_ZONE))
    return timezone.localtime(timezone.now())

def get_sum_of_feedbacks_duration(feedbacks):
    """Sum all given feedbacks duration.

    Args:
        feedbacks (list): A list of `models.Feedbacks`

    Returns:
        `datetime.timedelta`: The sum of all feedbacks duration.

    """
    total_duration = timedelta(0)
    for feedback in feedbacks:
        total_duration += feedback.duration
    return total_duration
