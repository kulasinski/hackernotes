from pydantic import BaseModel

from ..annotations import Annotations

class Snippet(BaseModel):
    content: str
    annotations: Annotations = Annotations()

    # --- Serialization Methods ---
    def dumps(self) -> str:
        """Serialize the snippet to a string."""
        # NOTE: The annotations are serialized at the Note level.
        return self.content.strip() 
    
    @classmethod
    def loads(cls, content: str) -> "Snippet":
        """Deserialize the snippet from a string."""
        annotations = Annotations() # TODO
        return Snippet(content=content.strip(), annotations=annotations)