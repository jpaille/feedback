from collections import namedtuple
from datetime import date

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.dateformat import DateFormat
from feedback.models import Feedback, Subject
from feedback.utils import previous_monday_date, get_sum_of_feedbacks_duration, next_monday_date
from stats.utils import get_lost_info_percentage


def create_feedbacks_scheduler_report_template_context(scheduler_reports):
    validated_feedbacks = [scheduler_report for scheduler_report in scheduler_reports if scheduler_report.done]
    failed_feedbacks = [scheduler_report for scheduler_report in scheduler_reports if not scheduler_report.done]
    return {"validated_feedbacks" : validated_feedbacks,
            "failed_feedbacks": failed_feedbacks,
            "report_scheduler_start_date" : previous_monday_date(),
            "report_scheduler_end_date" : date.today()}

def create_subjects_memory_states_template_context():
    SubjectMemoryState = namedtuple('SubjectProgressState', ['subject',
                                                             'retained_info_percentage', 'lost_info_percentage'])
    subjects = Subject.objects.all()
    subjects_memory_states = []
    for subject in subjects:
        lost_info_percentage = get_lost_info_percentage(subject)
        subjects_memory_states.append(SubjectMemoryState(subject.title,
                                                         100 - lost_info_percentage,
                                                         lost_info_percentage))
    return {"subjects_memory_states" : subjects_memory_states}

def create_next_week_feedback_sessions_template_context():
    next_week_feedbacks = Feedback.objects.filter(date=next_monday_date())
    return {"next_week_feedbacks" : next_week_feedbacks,
            "next_week_total_feedbacks_duration" : get_sum_of_feedbacks_duration(next_week_feedbacks)}



def send(feedback_scheduler_reports):
    context = {}
    context.update(create_feedbacks_scheduler_report_template_context(feedback_scheduler_reports))
    context.update(create_subjects_memory_states_template_context())
    context.update(create_next_week_feedback_sessions_template_context())
    mail_content = render_to_string('mail_reports/base.html', context)
    msg = EmailMessage("Feedback updates for the week of {}".format(DateFormat(previous_monday_date()).format("F jS, Y")),
                       mail_content, "feedback@locahost.com", [settings.EMAIL_HOST_USER])
    msg.content_subtype = "html"
    msg.send()
