from typing import Set
from .annotation import Annotation

TAG_PATTERN: str = r"#([\w-]+|\"[^\"]+\")"

class Tag(Annotation):
    """Tag annotation model."""
    content: str

    # --- Serializaton Methods ---
    def __hash__(self):
        return self.content.__hash__()

    def dumps(self) -> str:
        """Serialize the tag to a string."""
        return '#'+self.content.strip()
    
    @classmethod
    def loads(cls, content: str) -> "Tag":
        """Deserialize the tag from a string."""
        return Tag(content=content.strip())
    
    # --- Logical Methods ---

    @classmethod
    def extract(cls, content: str) -> Set["Tag"]:
        """Extract tags from the content."""
        import re
        tags = set()
        for tag in re.findall(TAG_PATTERN, content):
            tags.add(Tag(content=tag))
        return tags
    
    def occurs(self, content: str) -> bool:
        """Check if the tag occurs in the given content."""
        return f"#{self.content}" in content