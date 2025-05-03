from typing import Set
from pydantic import BaseModel

from hackernotes.core.annotations import Annotations
from hackernotes.core.annotations.entity import Entity
from hackernotes.core.annotations.tag import Tag

from .snippet import Snippet

class Snippets(BaseModel):
    """
    A collection of code snippets held as dict: {<ord>: Snippet}
    """
    __snippets__: dict[int, Snippet] = {}

    # --- Properties ---

    @property
    def length(self):
        """Returns the number of snippets."""
        return len(self.__snippets__)
    
    @property
    def tags(self) -> Set[Tag]:
        """Returns the tags of the snippets."""
        tags = set()
        for snippet in self.__snippets__.values():
            tags.update(snippet.annotations.tags)
        return tags
    
    @property
    def entities(self) -> Set[Entity]:
        """Returns the tags of the snippets."""
        entities = set()
        for snippet in self.__snippets__.values():
            entities.update(snippet.annotations.entities)
        return entities
    
    @property
    def last_snippet(self) -> Snippet:
        """Returns the last snippet."""
        if self.length == 0:
            return None
        return self.__snippets__[self.length - 1]
    
    # --- Overridden Methods ---

    def __getitem__(self, key: int) -> Snippet:
        """Returns the snippet at the given index."""
        return self.__snippets__[key]
    
    def __setitem__(self, key: int, value: Snippet):
        """Sets the snippet at the given index."""
        self.__snippets__[key] = value

    def __delitem__(self, key: int):
        """Deletes the snippet at the given index."""
        del self.__snippets__[key]
        self.__snippets__ = {k: v for k, v in self.__snippets__.items() if k != key}
        # Re-index the snippets
        self.reindex()

    def __iter__(self):
        """Iterates over the snippets."""
        for key in self.__snippets__:
            yield self.__snippets__[key]

    def __contains__(self, content: str) -> bool:
        """Checks if the snippet with a given content exists."""
        for snippet in self.__snippets__.values():
            if snippet.content in content:
                return True
        return False
            
    def __len__(self) -> int:
        """Returns the number of snippets."""
        return self.length
    
    # --- Logical Methods ---

    def add(self, content: str) -> Snippet:
        """Adds a new snippet to the collection."""
        annotations = Annotations.extract(content)
        snippet = Snippet(content=content, annotations=annotations)
        self[self.length] = snippet
        return snippet
    
    def update(self, ord: int, content: str) -> Snippet:
        """Updates an existing snippet with new content"""
        annotations = Annotations.extract(content)
        snippet = Snippet(content=content, annotations=annotations)
        self[ord] = snippet
        return snippet
    
    def remove(self, ord: int) -> None:
        del self[ord]
        self.reindex()

    def reindex(self):
        """Re-indexes the snippets."""
        snippets = {i: snippet for i, snippet in enumerate(self)}
        self.__snippets__ = snippets

    # --- Serialization Methods ---

    def dumps(self) -> str:
        """Serializes the snippets to a string."""
        return "\n\n".join(
            f"[{ord}] {snippet.dumps()}" for ord, snippet in self.__snippets__.items()
        )+"\n\n"
    
    @classmethod
    def loads(cls, data: str, ext_annotations: Annotations = None) -> "Snippets":
        """Deserializes the snippets from a string."""
        import re
        snippets = Snippets()
        lines = data.split("\n\n")
        for line in lines:
            if line.strip():
                # use regex to extract the [d+] first occurrence
                match = re.match(r"\[(\d+)\]\s*(.*)", line)
                if not match:
                    raise ValueError(f"Invalid snippet format: {line}")
                ord = match.group(1)
                content = match.group(2)
                snippet = Snippet.loads(content, ext_annotations=ext_annotations)
                snippets[int(ord)] = snippet

        return snippets
        

    