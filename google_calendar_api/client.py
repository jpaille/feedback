"""A small client using google calendar api.

This module contains functions to get, create or update calendar events.
"""

from collections import namedtuple
import datetime
import json
import uuid

from apiclient import discovery
from django.conf import settings
from googleapiclient.errors import HttpError
import httplib2

from oauth2client.client import OAuth2Credentials

class GoogleCalendarClient(object):
    def __init__(self):
        with open("oauth_credentials.json", "r") as oauth_credentials_file:
            oauth_credentials = json.loads(oauth_credentials_file.read())
            credentials = OAuth2Credentials(**oauth_credentials)
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('calendar', 'v3', http=http)
            self.service = service

    def create_event(self, summary, date, last_feedback_duration=datetime.timedelta(0), color_id=2):
        date = date.strftime("%Y-%m-%d")
        event = {
            'summary': summary,
            'location': ':'.join(str(last_feedback_duration).split(':')[:2]), ## remove seconds
            'colorId' : color_id,
            'start': {'date': date},
            'end': {'date': date},
            'reminders' : {'useDefault': 'False',
                           'overrides' : []} ## disable notification.
        }
        event = self.service.events().insert(calendarId='primary',
                                             body=event).execute()
        return event

    def get_event(self, event_id):
        event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
        return event

    def update_event(self, event_id, fields):
        event = self.service.events().patch(calendarId='primary', eventId=event_id, body=fields).execute()
        return event

    def delete_event(self, event_id):
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()

class GoogleCalendarTestClient(GoogleCalendarClient):
    def __init__(self):
        """
        Online test client. We use fake google account.
        Credentials : username: feedbacktestcase@gmail.com
                      password: feedback2
        """
        test_credentials = {"access_token" : "ya29.Ci9mA9zgQeI3NpFzjUKvWtT4feha1ueG3TU1ONoEXDEJYhE_1LLzR1gwZwJVkkWmRg",
                            "client_id" : "548625985977-at30f2k5kj54ibbe44r6k579be3vu6pr.apps.googleusercontent.com",
                            "client_secret" : "glhxKw_I3t99IDl7gz2DVWi4",
                            "refresh_token" : "1/bfBlAWZAfDd4p2ZSb0i1HFO08xHktDQtWzxBpOhEqFI",
                            "token_expiry" : 3600,
                            "token_uri" : "https://www.googleapis.com/oauth2/v4/token",
                            "user_agent" : "Feedbacks application"}
        credentials = OAuth2Credentials(**test_credentials)
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        self.service = service

class GoogleCalendarOfflineClient(object):
    def __init__(self):
        self.events = {}

    def create_event(self, summary, date, last_feedback_duration=0, color_id='2'):
        event = {"id" : uuid.uuid4().hex,
                 "summary": summary,
                 "start": {u'date': date.strftime("%Y-%m-%d")},
                 "end": {u'date': date.strftime("%Y-%m-%d")},
                 'location': ':'.join(str(last_feedback_duration).split(':')[:2]), ## remove seconds
                 'colorId' : color_id,
                 'reminders' : {'useDefault': 'False', 'overrides' : [{}]}, ## disable notification.
                 "status" : "confirmed"}
        self.events[event["id"]] = event
        return event

    def get_event(self, event_id):
        event = self.events.get(event_id, None)
        if not event:
            raise HttpError(namedtuple('resp', ['status', 'reason'])(status=404, reason=""), content="", uri="")
        else:
            return event
    def update_event(self, event_id, fields):
        self.events[event_id].update(fields)
        return self.events[event_id]

    def delete_event(self, event_id):
        """"
        When we delete an event Google switch the event  status to `cancelled`,  but keep it the database.
        We will adopt the same behaviour in the offlineclien.
        """
        self.events[event_id]["status"] = "cancelled"

def get_google_calendar_client():
    """
    Return the right google calendar client according to the GOOGLE_CALENDAR_CLIENT setting.
    So far there is three possible clients:
        - `GoogleCalendarClient`: A client that uses personnal credentials stores in feedbacks/oauth_credentials.json
        - `GoogleCalendarTestClient`: A client that uses a test google account.
        - `GoogleCalendarOfflineClient`:  A complete a offline client. Used while testing to avoid api calls.
    """
    return settings.GOOGLE_CALENDAR_CLIENT()
