
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