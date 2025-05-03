from typing import Set
from .annotation import Annotation
from ..types import EntityType

ENTITY_PATTERN: str = r"(?<!\w)@\w+"

class Entity(Annotation):
    """Entity annotation model."""
    content: str
    type: EntityType = EntityType.UNKNOWN

    # --- Logical Methods ---

    @classmethod
    def extract(cls, content: str) -> Set["Entity"]:
        """Extract entities from the content."""
        import re
        entities = set()
        for entity in re.findall(ENTITY_PATTERN, content):
            entities.add(Entity(content=entity[1:]))
        return entities
    
    def occurs(self, content: str) -> bool:
        """Check if the entity occurs in the given content."""
        return f"@{self.content}" in content

    # --- Serializaton Methods ---
    def __hash__(self):
        return self.dumps(prefix=False).__hash__()

    def dumps(self, prefix=True, content_only: bool = False) -> str:
        """Serialize the tag to a string."""
        output = f'{"@" if prefix else ""}{self.content.strip()}'
        if content_only:
            return output
        else:
            return f'{output} ({self.type.value})'
    
    @classmethod
    def loads(cls, content: str) -> "Entity":
        """Deserialize the tag from a string."""
        try:
            if content.startswith('@'):
                content = content[1:]
            # TODO use regex
            splt = content.strip().split("(")
            e_value = splt[0].strip()
            e_type = splt[1].replace(")","").strip().upper()
        except:
            raise ValueError(f"A weird entity to parse: {content}")
        return Entity(content=e_value, type=e_type)
    
    def __repr__(self):
        return '<ENTITY> '+self.dumps(prefix=False)
    
    def __str__(self):
        return '<ENTITY> '+self.dumps(prefix=False)