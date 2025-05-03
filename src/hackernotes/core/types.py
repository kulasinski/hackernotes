from enum import Enum

from pydantic import BaseModel

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

class EntityType(HackerEnum):
    UNKNOWN = "UNKNOWN"
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"

class EntityIntelligence(BaseModel):
    """
    Represents an entity extracted from a note.
    """
    value: str
    type: EntityType

    # define hash
    def __hash__(self):
        return hash((self.value, self.type))

class ExtractedEntities(BaseModel):
    """
    Represents a collection of extracted entities.
    """
    entities: list[EntityIntelligence]

class TimeIntelligence(BaseModel):
    """
    Represents time intelligence extracted from a note.
    - literal: The literal representation of the time intelligence in the note, e.g. "next week".
    - value: The actual value of the time intelligence, e.g. "2023-10-15".
    - scope: The time scope of the intelligence, e.g. "WEEK", "DAY", etc.
    """
    literal: str
    value: str
    scope: TimeScope

class ExtractedTimeIntelligence(BaseModel):
    """
    Represents a collection of extracted time intelligence.
    """
    time_intelligence: list[TimeIntelligence]