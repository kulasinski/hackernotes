
# --- TAG PARSING ---

from typing import List

from hackernotes.core.types import EntityIntelligence, EntityType
from hackernotes.utils.term import print_err


def line2tags(text: str) -> set:
    """
    Convert a line of text into a set of tags. Assume the text is space-delimited and each tag starts by hash '#'.
    """
    # Split the text by commas and strip whitespace
    tags = {tag.strip() for tag in text.split('#') if tag.strip()}
    
    # Remove empty tags
    tags.discard('')
    
    return tags

def tags2line(tags: set) -> str:
    """
    Convert a set of tags into a line of text. Each tag is separated by a space and starts with a hash '#'.
    """
    # Join the tags with commas and add a hash at the beginning of each tag
    return ' '.join(f'#{tag}' for tag in tags)

# --- ENTITY PARSING ---

def line2entities(text: str) -> List[EntityIntelligence]:
    """
    Convert a line of text into a list of entities. Assume the text is space-delimited and each entity starts by '@'.
    """
    # Split the text by commas and strip whitespace
    tuples = [t.strip() for t in text.split('@') if t.strip()]

    # Parse tuples
    tuples_parsed = []
    for t in tuples:
        # Split the entity into value and type
        parts = t.split(':')
        if len(parts) == 2:
            value = parts[0].strip()
            entity_type = parts[1].strip()
            # Validate entity type
            try:
                entity_type = EntityType[entity_type.upper()]
            except KeyError:
                print_err(f"Invalid entity type: {entity_type}")
                continue
            tuples_parsed.append((value, entity_type))
        else:
            print_err(f"Invalid entity format: {t}")
            continue
        
    entities = [
        EntityIntelligence(
            value=t[0],
            type=t[1]
        )
        for t in tuples_parsed
    ]

    return entities

def entities2line(entities: List[EntityIntelligence]) -> str:
    """
    Convert a list of entities into a line of text. Each entity is separated by a space and starts with an '@'.
    """
    # Join the entities with commas and add an '@' at the beginning of each entity
    return ' '.join(f'@{entity.value}:{entity.type.name}' for entity in entities)