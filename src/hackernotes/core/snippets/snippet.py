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
    def loads(cls, content: str, ext_annotations: Annotations = None) -> "Snippet":
        """Deserialize the snippet from a string."""
        annotations = Annotations()
        if ext_annotations:
            # Filter the annotations to only include those that are in the snippet
            annotations.tags = {tag for tag in ext_annotations.tags if tag.occurs(content)}
            # TODO etc.
        return Snippet(content=content.strip(), annotations=annotations)