# Modulos de python
from datetime import datetime, timedelta
import datetime

# Modulo de python_timezone
import pytz


def get_timezone():
    """
    Obtenemos la hora local

    """
    return datetime.datetime.now(tz=pytz.timezone('America/Mexico_City'))


def get_timedelta(days=0, minutes=0):
    """
    De la hora local obtenida, definimos los dias o minutos que van
    a suceder en el futuro

    """

    return get_timezone() + datetime.timedelta(days=days, minutes=minutes)
