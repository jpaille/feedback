from django.contrib import admin
from django.conf import settings

from feedback.models import Subject, Feedback, GoogleCalendarFeedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("subject", "done", "duration", "date")

class GoogleCalendarFeedbackAdmin(admin.ModelAdmin):
    list_display = ("subject", "duration", "date", "event_id")

admin.site.register(Subject)

if settings.USE_GOOGLE_CALENDAR:
    admin.site.register(GoogleCalendarFeedback, GoogleCalendarFeedbackAdmin)
else:
    admin.site.register(Feedback, FeedbackAdmin)
