# Modulos de python
from datetime import datetime, timedelta
import datetime

# Modulo de python_timezone
import pytz


def get_timezone():
    # date_now = datetime.datetime.now(tz=pytz.timezone('America/Mexico_City'))
    return datetime.datetime.now(tz=pytz.timezone('America/Mexico_City'))


def get_timedelta(days=0, minutes=0):
    exp = get_timezone() + datetime.timedelta(days=days, minutes=minutes)
    return exp
