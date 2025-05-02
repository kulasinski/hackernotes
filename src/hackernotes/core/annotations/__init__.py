from datetime import datetime
import re
from typing import List, Set, Tuple

from pydantic import BaseModel

from .tag import Tag

# Regex for extracting tags (#tag) and entities (@entity)

KEYWORD_PATTERN = r"@([\w-]+|\"[^\"]+\")"
URL_PATTERN = r'(https?://\S+|www\.\S+|\S+\.\S+)'

def extract_tags_and_entities(text: str) -> Tuple[set, set]:
    """Extracts tags and entities from text."""
    tags = re.findall(TAG_PATTERN, text)
    entities = re.findall(KEYWORD_PATTERN, text)
    return set(tags), set(entities)

def extract_urls(text: str) -> set:
    """Extracts URLs from text."""
    urls = re.findall(URL_PATTERN, text, re.IGNORECASE)
    return set(urls)

def containsTagsOnly(text: str):
    """Returns True if the text contains only tags."""
    tokens = text.split()
    for token in tokens:
        if not token.startswith("#"):
            return False
    return True

class Annotations(BaseModel):
    """Note annotations model."""
    tags: Set[Tag] = set()
    # entities: Set[Entity] = set()
    # times: Set[Time] = set()
    # urls: Set[URL] = set()

    # --- Logical Methods ---
    @classmethod
    def extract(cls, content: str) -> "Annotations":
        """Extract tags and entities from the content."""
        return cls(
            tags=Tag.extract(content),
            # TODO etc.
            # entities=cls.extract_entities(content),
            # times=cls.extract_times(content),
            # urls=cls.extract_urls(content)
        )

    # --- Tags Methods ---
    def add_tag(self, content: str|Tag) -> None:
        """Add a tag to the annotations."""
        if isinstance(content, str):
            self.tags.add(Tag(content=content))
        elif isinstance(content, Tag):
            self.tags.add(content)

    def has_tag(self, content: str) -> bool:
        """Check if the annotations contain a tag."""
        return any(tag.content == content for tag in self.tags)

    # TODO serialize and deserialize tags here

    # --- Serialization Methods ---
    
    def dumps(self) -> str:
        """Serialize the annotations to a string."""
        tags_serialized = ' '.join([tag.dumps() for tag in self.tags]).strip()
        data = f"[TAGS] {tags_serialized}\n"
        # etc. data += f"[ENTITY] {entity..}\n"
        return data
    
    @classmethod
    def loads(cls, content: str) -> "Annotations":
        """Deserialize the annotations from a string."""
        tags = set()
        # entities = set()
        # times = set()
        # urls = set()
        
        lines = content.split("\n")
        for line in lines:
            if line.startswith("[TAGS]"):
                tags_data = line[len("[TAGS]"):].strip()
                tags = {Tag.loads(tag) for tag in tags_data.split("#") if tag.strip()}
        
        return cls(tags=tags)