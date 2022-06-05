from datetime import datetime
from django.utils.timezone import make_aware


def format_datetime_str(val: str):
    form = "%Y-%m-%d %H:%M"
    date_time = datetime.strptime(val, form)
    date_time = make_aware(date_time)
    return date_time
