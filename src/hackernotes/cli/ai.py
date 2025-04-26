import click
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import HTML

from hackernotes.core.ai import extract_entities_from_text, extract_tags_from_text, extract_time_intelligence_from_text
from hackernotes.db import SessionLocal
from hackernotes.db.query import NoteCRUD
from hackernotes.utils.parsers import line2tags, tags2line
from hackernotes.utils.term import fsys, ftag, print_warn

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
    
    with SessionLocal() as session:
        note = NoteCRUD.get(session, note_id)

        note_body = note.title + "\n\n" + '\n'.join([snippet.content for snippet in note.snippets])

        if tags:
            tag_set = extract_tags_from_text(note_body)
        else:
            tag_set = None

        if entities:
            entity_intelligence = extract_entities_from_text(note_body)
        else:
            entity_intelligence = None

        if times:
            time_intelligence = extract_time_intelligence_from_text(note_body)
        else:
            time_intelligence = None
        
        if interactive:
            # Tags
            prompt_session = PromptSession(history=InMemoryHistory())
            tags_interactive = prompt_session.prompt(
                    HTML(f"<ansicyan>Tags (edit):</ansicyan> "),
                    default=tags2line(tag_set),
            )
            tag_set = line2tags(tags_interactive)
            # Entities
            # TODO
            # Time intelligence
            # TODO 

        else:
            # Tags
            if tag_set:
                print(fsys("Tags:"), ftag(tags2line(tag_set), decorator=""))
            # Entities
            # TODO
            # Time intelligence
            # TODO 

        # Add all (or selected) annotations to the note
        NoteCRUD.update(
            session, 
            note_id, 
            tags=tag_set, 
            entities=entity_intelligence, 
            times=time_intelligence
        )

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