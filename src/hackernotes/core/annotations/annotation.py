from pydantic import BaseModel

class Annotation(BaseModel):
    """Base class for annotations."""
    content: str

    def dumps(self) -> str:
        """Serialize the annotation to a string. This method should be overridden in subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")
    
    def loads(self, content: str):
        """Deserialize the annotation from a string. This method should be overridden in subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")