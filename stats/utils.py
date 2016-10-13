from feedback.models import Feedback

def get_feedback_progress(feedbacks):
    nbr_of_feedbacks = len(feedbacks)
    if nbr_of_feedbacks > 10:
        return 100
    else:
        return nbr_of_feedbacks * 10

def get_lost_info_percentage(subject):
    nbr_of_feedbacks = Feedback.objects.filter(subject=subject, _done=True).count()
    if nbr_of_feedbacks == 0 or subject.penalties == 0:
        return 0;
    if nbr_of_feedbacks - subject.penalties < 0:
        return 100
    return 100 - round(float(100) * (nbr_of_feedbacks - subject.penalties) / nbr_of_feedbacks, 1)
