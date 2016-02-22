from collections import namedtuple
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

Duration  = namedtuple('Duration', ['hours', 'minutes'])

def get_hours_and_minutes_from_timedelta(timedelta):
    """
    Convert timedelta seconds in hours and minutes.

    Returns:
        `Duration` (hours, minutes)
    """

    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return Duration(hours, minutes)

def get_sum_of_feedbacks_duration(feedbacks):
    """Take a list of `models.Feedbacks` and return the sum of
       all feedbacks session duration.
    """
    total_duration = timedelta(0)
    for feedback in feedbacks:
        total_duration += feedback.duration
    return get_hours_and_minutes_from_timedelta(total_duration)
