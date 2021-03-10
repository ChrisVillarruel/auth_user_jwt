from datetime import datetime


def msg_error(message, status, code, detail=None):
    if detail is None:
        detail = 'Error no detallado'

    msg_error = {
        'message': message,
        'status': status,
        'code': code,
        'date': datetime.now().strftime("%d-%m-%Y"),
        'diagnosticMessages': detail
    }
    return msg_error
