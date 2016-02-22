from django import template

register = template.Library()

def get_progress_color(value):
    """ Return the right html boostrap attribute for the
       progress bar.
     """
    if value == 100:
        return "progress-bar-success"
    elif value < 30:
        return "progress-bar-danger"
    elif value >= 30 and value < 70:
        return "progress-bar-warning"
    elif value >= 70  and value < 100:
        return "progress-bar-info"

register.filter('get_progress_color', get_progress_color)
