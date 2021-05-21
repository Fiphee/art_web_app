from django import template
from datetime import datetime, timezone

register = template.Library()


@register.filter
def how_long_ago(created_at):
    time_ago = datetime.now(timezone.utc) - created_at
    times = str(time_ago).split(',')
    if len(times) > 1:
        nr_of_days = int(times[0].split(' ')[0])
        weeks, days = divmod(nr_of_days, 7)
        if weeks:
            years, weeks = divmod(weeks, 52)
            if years:
                return f'{years}y'
            return f'{weeks}w'
        return f'{days}d'

    hours, minutes, seconds = times[0].split(':')
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds.split('.')[0])
    if hours:
        return f'{hours}h'
    if minutes:
        return f'{minutes}m'
    return f'{seconds}s'