from datetime import datetime
import pytz


def get_current_time() -> str:
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    return now.strftime('%H:%M:%S %d.%m.%Y')
