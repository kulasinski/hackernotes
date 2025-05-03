
from colorama import Fore

from hackernotes.core.note import Note
from hackernotes.core.snippets import Snippets
from hackernotes.core.snippets.snippet import Snippet
from hackernotes.utils.datetime import dt_dumps
from hackernotes.utils.term import fentity, fsys, ftag


def display_snippet(ord: int, snippet: Snippet):
    """Displays a single snippet in a formatted way."""
    
    snippet_content = snippet.content

    # Highlight tags and entities
    for tag in snippet.annotations.tags:
        snippet_content = snippet_content.replace(tag.dumps(prefix=True), ftag(tag.content))

    for entity in snippet.annotations.entities:
        print("replacing",entity.dumps(prefix=True, content_only=True),"with",fentity(entity.dumps(prefix=False)), entity.content)
        snippet_content = snippet_content.replace(entity.dumps(prefix=True, content_only=True), fentity(entity.dumps(prefix=False)))
    
    # Highlight times # TODO !!!

    # Highlight URLs # TODO ???
    # for url in snippet.urls:
    #     snippet_content = snippet_content.replace(url, f"{Fore.LIGHTBLACK_EX}{url}{Style.RESET_ALL}")

    # Display snippet
    print(fsys(f"[{ord}]"), snippet_content)

def display_snippets(snippets: Snippets):
    """Displays all snippets in a formatted way."""
    for ord, snippet in enumerate(snippets, start=0):
        display_snippet(ord, snippet)

def display_note(note: Note, width: int = 80, footer: bool = True):
    """Displays the note in a formatted way."""
    print("\n"+"=" * width)
    print(fsys("Title: ")+note.meta.title)
    print(fsys("ID: ")+note.meta.id)
    print(fsys(f"Created at: {dt_dumps(note.meta.created_at)}"))
    print(fsys(f"Last modified: {dt_dumps(note.meta.updated_at)}"))
    print("-" * width)

    # (Re)-order snippets by position # TODO necessary??
    # self.snippets = sorted(self.snippets, key=lambda x: x.position)

    # Display snippets
    display_snippets(note.snippets)
        
    if footer:
        print("-" * width)
        if note.annotations.tags:
            print(fsys("[TAGS] ")+ftag(note.annotations.tags_serialized))
        if note.annotations.entities:
            print(fsys("[ENTITIES] ")+fentity(note.annotations.entities_serialized))
        # if self.timesAll: # TODO 
        #     print(fsys("Times: ")+', '.join([f"{time.literal} ({time.scope})" for time in self.timesAll]))
        # if self.urls: # TODO ??
        #     print(fsys("URLs: ")+', '.join([f"{Fore.LIGHTBLACK_EX}{url.value}{Style.RESET_ALL}" for url in self.urls]))

        print("=" * width + "\n")
