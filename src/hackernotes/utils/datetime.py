from datetime import datetime

dateFormat = "%Y-%m-%d %H:%M:%S"

INPUT_DATE_FORMATS = [
    dateFormat,
    "%Y-%m-%d",
    "%d.%m.%Y",
]

def now(descriptive: bool = False) -> str:
    """Returns the current date and time in the format YYYY-MM-DD HH:MM:SS."""
    if descriptive:
        """ Return it in this way, e.g.: Tuesday, 10 October 2023, 12:00:00 AM """
        return datetime.now().strftime("%A, %d %B %Y, %I:%M:%S %p")
    else:
        return datetime.now().strftime(dateFormat)
    
def dt_dumps(dt: datetime) -> str:
    """Serialize a datetime object to a string."""
    return dt.strftime(dateFormat)

def dt_loads(dt_str: str) -> datetime:
    """Deserialize a string to a datetime object."""
    return datetime.strptime(dt_str, dateFormat)