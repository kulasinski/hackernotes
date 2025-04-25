import click

from hackernotes.core.ai import extract_entities_from_text, extract_tags_from_text, extract_time_intelligence_from_text
from hackernotes.db import SessionLocal
from hackernotes.db.query import NoteCRUD
from hackernotes.utils.term import print_warn

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
@click.option('--time', '-ti', is_flag=True, help="Highlight or add time intelligence to the note.")
def run(note_id, interactive, tags, entities, time):
    """Run an AI-magick task on a note."""
    if not note_id:
        print_warn("Note ID is required.")
        return
    
    if not any([tags, entities, time]):
        print_warn("At least one of --tags or --entities must be specified.")
        return
    
    with SessionLocal() as session:
        note = NoteCRUD.get(session, note_id)
    note_body = note.title + "\n\n" + '\n'.join([snippet.content for snippet in note.snippets])

    if tags: # TODO
        tag_set = extract_tags_from_text(note_body)
        print("Tags:",tag_set)

    if entities: # TODO
        entities = extract_entities_from_text(note_body)
        print("Entities:",entities)

    if time: # TODO
        # Placeholder for time intelligence logic
        time_intelligence = extract_time_intelligence_from_text(note_body)
        print("Time Intelligence:", time_intelligence)
    
    if interactive:
        # Placeholder for interactive mode logic
        print("Running in interactive mode... Agree or edit before applying")

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