from .annotation import Annotation

class Tag(Annotation):
    """Tag annotation model."""
    content: str
    
    # --- Serializaton Methods ---
    def __hash__(self):
        return self.content.__hash__()

    def dumps(self) -> str:
        """Serialize the tag to a string."""
        return self.content.strip()
    
    @classmethod
    def loads(cls, content: str) -> "Tag":
        """Deserialize the tag from a string."""
        return Tag(content=content.strip())