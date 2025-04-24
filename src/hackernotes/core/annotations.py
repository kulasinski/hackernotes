from datetime import datetime
import re
from typing import List, Tuple

# Regex for extracting tags (#tag) and entities (@entity)
TAG_PATTERN = r"#([\w-]+|\"[^\"]+\")"
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