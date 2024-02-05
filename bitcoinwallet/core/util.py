from datetime import datetime

from definitions import FORMAT


def datetime_now() -> str:
    return datetime.now().strftime(FORMAT)
