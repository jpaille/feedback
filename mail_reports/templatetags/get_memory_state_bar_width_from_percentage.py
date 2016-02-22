from django import template

register = template.Library()

def get_memory_state_bar_width_from_percentage(value):
    """
    Return the right progress bar width for a corresponding subject progression percentage.
    """

    full_bar_width = 380
    return (value * 380) / 100

register.filter('get_memory_state_bar_width_from_percentage', get_memory_state_bar_width_from_percentage)
