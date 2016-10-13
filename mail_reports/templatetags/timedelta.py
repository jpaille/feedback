from django import template

register = template.Library()

def timedelta(value):
    """Format a `timedelta` duration.

    Example:
        Convert 2 hours and 30 minutes duration into a string.

        >>> timedelta(hours=2, minutes=30)
        '2h30'

    """

    hours, remainder = divmod(value.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours == 0:
        return "{}mins".format(minutes)
    if minutes == 0:
        return "{}h".format(hours)
    if 0 < minutes < 10:
        minutes = "0{}".format(minutes)
    return "{}h{}".format(hours, minutes)

register.filter('timedelta', timedelta)
