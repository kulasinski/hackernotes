

from pydantic import BaseModel

from .annotations import Annotations

class Snippet(BaseModel):
    content: str
    annotations: Annotations = Annotations()

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

    def reindex(self):
        """Re-indexes the snippets."""
        self.__snippets__ = {i: self.__snippets__[i] for i in range(len(self.__snippets__))}

    