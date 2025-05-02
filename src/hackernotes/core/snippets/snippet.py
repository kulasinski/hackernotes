from pydantic import BaseModel

from hackernotes.core.annotations.tag import Tag

from ..annotations import Annotations
import re

class Snippet(BaseModel):
    content: str
    annotations: Annotations = Annotations()

    # --- Annotations Methods ---
    def prefix_tag(self, tag_value: str) -> None:
        """ Adds # to each occurrence of the tag in the snippet content. The tag value should not contain #. """
        pattern = r'\b' + re.escape(tag_value) + r'\b'
        self.content = re.sub(pattern, f"#{tag_value}", self.content)

    def add_tag(self, tag: Tag) -> None:
        """ Adds a tag to the snippet. """
        if tag.content.startswith("#"):
            tag.content = tag.content[1:]

        self.prefix_tag(tag.content)
        self.annotations.add_tag(tag.content)

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