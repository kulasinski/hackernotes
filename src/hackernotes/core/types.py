from enum import Enum

class HackerEnum(Enum):
    """
    Base class for all enums in the HackerNotes project.
    """
    @classmethod
    def to_list(cls) -> list[str]:
        """
        Convert the enum values to a list of strings.
        """
        return [item.value for item in cls]
    
    @classmethod
    def to_str(cls) -> str:
        """
        Convert the enum values to a comma-separated string.
        """
        return ", ".join([f"'{v}'" for v in cls.to_list()])

class TimeScope(HackerEnum):
    CENTURY = "CENTURY"
    YEAR = "YEAR"
    MONTH = "MONTH"
    WEEK = "WEEK"
    DAY = "DAY"
    HOUR = "HOUR"
    MINUTE = "MINUTE"
    SECOND = "SECOND"
    MILLISECOND = "MILLISECOND"
    
class PromptType(HackerEnum):
    CHAT = "CHAT"
    GENERATE = "GENERATE"
    ANNOTATE = "ANNOTATE"
    CLASSIFY = "CLASSIFY"

class TaskStatus(HackerEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"