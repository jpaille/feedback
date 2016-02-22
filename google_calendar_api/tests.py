from datetime import date

from django.test import TestCase
from googleapiclient.errors import HttpError

from google_calendar_api.client import get_google_calendar_client

class GoogleCalendarTestClientTestCase(TestCase):
    def setUp(self):
        self.test_client = get_google_calendar_client()
        self.event = self.test_client.create_event("Test Event", date(2016, 9, 25))
    def test_create_event(self):
        self.assertEqual(self.event['summary'], "Test Event")
        self.assertEqual(self.event['start']['date'], "2016-09-25")
        self.assertEqual(self.event['end']['date'], "2016-09-25")
    def test_get_event(self):
        self.assertEqual(self.event["id"], self.test_client.get_event(self.event["id"])["id"])
    def test_update_event(self):
        self.assertNotEqual(self.event["start"]["date"], "2016-09-29")
        self.assertNotEqual(self.event["end"]["date"], "2016-09-29")
        fields = {"start" : {"date" : "2016-09-29"}, "end" :{"date" : "2016-09-29"}}
        updated_event = self.test_client.update_event(self.event["id"], fields)
        self.assertEqual(updated_event["start"]["date"], "2016-09-29")
        self.assertEqual(updated_event["end"]["date"], "2016-09-29")
    def test_delete_event(self):
        self.test_client.delete_event(self.event["id"])
        self.assertEqual("cancelled", self.test_client.get_event(self.event["id"])["status"])
    def tearDown(self):
        try:
            self.test_client.delete_event(self.event["id"])
        except HttpError:
            pass # the event has already been deleted.

# class GoogleCalendarTestOfflineClient(GoogleCalendarClientTestCase):
#     def setUp(self):
#         self.test_client = GoogleCalendarOfflineClient()
#         self.event = self.test_client.create_event("Test Event", date(2016, 9, 25))
