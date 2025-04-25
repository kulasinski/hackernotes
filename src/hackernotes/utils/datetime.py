from datetime import datetime

dateFormat = "%Y-%m-%d %H:%M:%S"

def now(descriptive: bool = False) -> str:
    """Returns the current date and time in the format YYYY-MM-DD HH:MM:SS."""
    if descriptive:
        """ Return it in this way, e.g.: Tuesday, 10 October 2023, 12:00:00 AM """
        return datetime.now().strftime("%A, %d %B %Y, %I:%M:%S %p")
    else:
        return datetime.now().strftime(dateFormat)