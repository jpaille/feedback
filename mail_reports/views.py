from datetime import date

from django.shortcuts import render
from feedback.feedbacks_scheduler import FeedbackSchedulerReport
from .send_reports import (create_feedbacks_scheduler_report_template_context,
                           create_subjects_memory_states_template_context,
                           create_next_week_feedback_sessions_template_context)

def test_report_template(request):
    feedback_scheduler_reports = [FeedbackSchedulerReport("Histoire de l'economie", False, date(year=2016, month=10, day=2)),
                                  FeedbackSchedulerReport("Histoire de France", False, date(year=2016, month=11, day=2)),
                                  FeedbackSchedulerReport("Histoire des instruments", True, date(year=2016, month=8, day=15)),
                                  FeedbackSchedulerReport("Physique", False, date(year=2016, month=10, day=18)),
                                  FeedbackSchedulerReport("Anglais", False, date(year=2016, month=10, day=2))]
    context = {}
    context.update(create_feedbacks_scheduler_report_template_context(feedback_scheduler_reports))
    context.update(create_subjects_memory_states_template_context())
    context.update(create_next_week_feedback_sessions_template_context())
    return render(request, 'mail_reports/base.html', context)
