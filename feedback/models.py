import datetime

from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.conf import settings
from googleapiclient.errors import HttpError
from polymorphic.models import PolymorphicModel

from google_calendar_api.client import get_google_calendar_client
from feedback.utils import next_monday_date, get_google_calendar_event_color_from_penalties

def get_feedback_class():
    if settings.USE_GOOGLE_CALENDAR:
        return GoogleCalendarFeedback
    return Feedback

class Subject(models.Model):
    title = models.CharField(max_length=30)
    nbr_of_cards = models.IntegerField()
    feedback_session_duration = models.DurationField(default=datetime.timedelta(hours=2))
    penalties = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def get_last_feedback(self):
        return Feedback.objects.filter(subject=self).last()

    def update_feedback_session_duration(self):
        self.feedback_session_duration = self.get_last_feedback().duration

    def update_penalties(self, is_feedback_done=False):
        if not is_feedback_done:
            self.penalties += 2
        elif is_feedback_done and self.penalties >= 2:
            self.penalties -= 2
        self.save()

@receiver(post_save)
def create_first_feedback(sender, instance, **kwargs):
    """
    When a subject is created the first feedback session is schedule the very the next week.
    """
    if type(instance) == Subject and not instance.get_last_feedback():
        get_feedback_class()(subject=instance, date=next_monday_date()).save()

class Feedback(PolymorphicModel):
    """"""
    subject = models.ForeignKey('Subject')
    date = models.DateField(default=datetime.datetime.now().date())
    _done = models.BooleanField(default=False)
    duration = models.DurationField(default=datetime.timedelta(hours=2))

    @property
    def done(self):
        return self._done

    @done.setter
    def done(self, value):
        self._done = value

class GoogleCalendarFeedback(Feedback):
    google_calendar_client = get_google_calendar_client()
    event_id = models.CharField(max_length=30) ## Google calendar event_id.

    __original_date = None

    def __init__(self, *args, **kwargs):
        super(GoogleCalendarFeedback, self).__init__(*args, **kwargs)
        self.__original_date = self.date

    @property
    def done(self):
        """
        Check if the feedback has been done. When a user has completed a feedback,
        he writes the "d" character in the description field of the google calendar interface.
        We assume that if we find the letter "d" in the description field the feedback has been done.
        """
        event = self.google_calendar_client.get_event(self.event_id)
        if event.get("description", None) and event["description"] == "d":
            self._done = True
            self.get_duration_field_from_calendar(event)
        return self._done

    @done.setter
    def done(self, value):
        self._done = value

    def save(self, *args, **kwargs):
        """
        Overload save method to interact with the google calendar.
        When a feedback is created we create a calendar event.
        When a feedback date is changed we update the corresponding calendar date.
        """
        if not self.pk: ## Ensure that the object doesn't exist already.
            self.event_id = self.google_calendar_client.create_event(self.subject.title,
                                                                     self.date,
                                                                     str(self.subject.feedback_session_duration),
                                                                     color_id=get_google_calendar_event_color_from_penalties(self.subject.penalties))["id"]
        else:
            if self.__original_date != self.date: ## This means that the feedback was postponed.
                self._update_calendar_event()
        super(GoogleCalendarFeedback, self).save(*args, **kwargs)

    def get_duration_field_from_calendar(self, event):
        """
        We want to enter the duration of the feedback session directly into google calendar.
        There is no duration field in the calendar event. So we will arbitrarily ask the user
        to put this data inside the `location` field. (`description` field is already taken)
        We extract the duration from the event and send it to the database.
        """
        duration = event.get("location", None)
        if not duration:
            return datetime.timedelta(hours=0)
        else:
            duration_time = datetime.datetime.strptime(duration, "%H:%M")
            self.duration = datetime.timedelta(hours=duration_time.hour, minutes=duration_time.minute)

    def _update_calendar_event(self):
        fields = {"start": {"date" : self.date.strftime("%Y-%m-%d")},
                  "end": {"date" : self.date.strftime("%Y-%m-%d")},
                  "colorId": get_google_calendar_event_color_from_penalties(self.subject.penalties)}
        self.google_calendar_client.update_event(self.event_id, fields)

@receiver(pre_delete)
def delete_event(sender, instance, **kwargs):
    if type(instance) == GoogleCalendarFeedback:
        try:
            instance.google_calendar_client.delete_event(instance.event_id)
        except HttpError:
            pass
