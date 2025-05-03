import click
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import HTML

from hackernotes.core.ai import extract_annotations
from hackernotes.core.annotations import Annotations
from hackernotes.core.annotations.entity import Entity
from hackernotes.core.note import Note
from hackernotes.core.types import EntityType
from hackernotes.db import SessionLocal
# from hackernotes.db.query import NoteCRUD
from hackernotes.utils.parsers import line2tags, tags2line
from hackernotes.utils.term import fsys, ftag, print_sys, print_warn

from . import hn

# === AI/LLM Commands ===
@hn.group()
def ai():
    """AI intelligence operations."""
    pass

@ai.command()
def queue():
    """List all queued tasks."""
    pass

@ai.command()
def dequeue():
    """Dequeue a task. Or all tasks if no task is specified."""
    pass

@ai.command()
@click.argument('note_id')
@click.option('--interactive', '-i', is_flag=True, help="Run in interactive mode. Agree to LLM intelligence.")
@click.option('--tags', '-t', is_flag=True, help="Highlight or add tags to the note.")
@click.option('--entities', '-e', is_flag=True, help="Highlight or add entities to the note.")
@click.option('--times', '-ti', is_flag=True, help="Highlight or add time intelligence to the note.")
def run(note_id, interactive, tags, entities, times):
    """Run an AI-magick task on a note."""
    if not note_id:
        print_warn("Note ID is required.")
        return
    
    if not any([tags, entities, times]):
        print_warn("At least one of --tags or --entities must be specified.")
        return
    
    note = Note.read(note_id)
    if not note:
        return
    
    note_body = note.snippets.dumps() # TODO other way?

    # Use AI to extract annotations
    new_annotations = extract_annotations(
        note_body,
        extract_tags=tags,
        extract_entitites=entities,
        ignore_tags=note.annotations.tags,
        ignore_entities={e for e in note.annotations.entities if e.type != EntityType.UNKNOWN}
    )
        
    if interactive:
        prompt_session = PromptSession(history=InMemoryHistory())

        # Tags
        if new_annotations.tags:
            tags_interactive = prompt_session.prompt(
                    HTML(f"<ansicyan>Tags (edit):</ansicyan> "),
                    default=tags2line(new_annotations.tags),
            )
            new_annotations.tags = line2tags(tags_interactive)

        # Entities
        if new_annotations.entities:
            entities_interactive = prompt_session.prompt(
                    HTML(f"<ansicyan>Entities (edit):</ansicyan> "),
                    default=new_annotations.entities_serialized,
            )
            entity_set = Annotations.entities_deserialize(entities_interactive)
        
        # Time intelligence
        # TODO 

    else:
        # Tags
        if new_annotations.tags:
            print(fsys("Tags:"), ftag(tags2line(new_annotations.tags), decorator=""))
        # Entities
        if entity_set:
            print(fsys("Entities:"), ftag(Annotations(entities=entity_set).entities_serialized, decorator=""))
        # Time intelligence
        # TODO 

    # Create new snippet with the remaining annotations
    ai_snippet_content = ""
    # Add the tags to the note, wherever they fit. 
    used_tags = set()
    if tags:
        for tag in new_annotations.tags:
            for snippet in note.snippets:
                if tag.content in snippet.content and not snippet.annotations.has_tag(tag):
                    snippet.add_tag(tag)
                    used_tags.add(tag)
                    break
        remaining_tags = new_annotations.tags - used_tags
        if remaining_tags:
            ai_snippet_content += tags2line(remaining_tags)
            # TODO add entities and time intelligence to the snippet content
    if entities:
        pass

    if ai_snippet_content:
        # Add the remaining (or selected) annotations to the note
        note.add(content=ai_snippet_content)

    # Display the updated note to the user
    print(note.dumps())

    if tags:
        # Inform about the changes
        print_sys("New tags to add to existing snippet: "+tags2line(used_tags))
        print_sys("New tags to add to new snippet: "+tags2line(remaining_tags))
    
    # Save to disk
    confirm = input(fsys("Do you want to save the changes? (y/n) "))
    if confirm.lower() != "y":
        print_warn("Changes not saved.")
        return
    note.persist()
    print_sys("Note has been updated.")

    return

@ai.command()
@click.argument('type')
def prompt(type):
    pass

@ai.command()
def chat():
    pass

@ai.command()
@click.argument('note_id')
def generate(note_id):
    pass