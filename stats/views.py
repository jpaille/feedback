from django.shortcuts import render
from feedback.models import Subject, Feedback
from stats.utils import get_feedback_progress

def dashboard(request):
    """Display stats about feedbacks"""
    
    subjects = Subject.objects.all()
    subjects_progression_dict = {}
    for subject in subjects:
        subjects_progression_dict[subject.title] = get_feedback_progress(Feedback.objects.filter(subject=subject))
    return render(request, 'stats/dashboard.html', context= {"subjects_progression" : subjects_progression_dict})



