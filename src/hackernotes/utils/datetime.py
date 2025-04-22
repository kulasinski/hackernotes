from datetime import datetime

dateFormat = "%Y-%m-%d %H:%M:%S"

def now():
    """Returns the current date and time in the format YYYY-MM-DD HH:MM:SS."""
    return datetime.now().strftime(dateFormat)