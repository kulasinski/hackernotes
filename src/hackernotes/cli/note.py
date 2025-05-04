import click
from tabulate import tabulate

from hackernotes.core.note import Note
from hackernotes.core.workspace import Workspace
from hackernotes.utils.display import display_note

from . import hn
from ..core.interactive import handle_create_note, handle_edit_note
# from ..core.note import NoteService
from ..db import SessionLocal
from ..utils.datetime import now
from ..utils.term import clear_terminal, print_warn

# === Note Commands ===
@hn.group()
def note():
    """Note-related operations."""
    # preflight() # Uncomment if needed
    pass

@note.command()
@click.argument('title', type=str, required=False, default=f'Untitled {now()}')
def new(title: str):
    """Create new note with optional title."""
    # with SessionLocal() as session:
    #   handle_create_note(session, title)
    handle_create_note(title)

@note.command()
@click.argument('note_id', required=False)
@click.option("--title", type=str, help="Fetch by the note title")
@click.option("--width", type=int, default=50, help="Set the width for displaying the note")
def show(note_id, title, width):
    """Show a note (last edited if none specified)."""
    # with SessionLocal() as session:
    if note_id:
        note = Note.read(note_id)
    elif title:
        # leverage workspace?
        raise NotImplementedError("Fetching by title is not implemented yet.")
    else:
        # leverage workspace?
        raise ValueError("Getting the last edited note is not implemented yet.")
    if not note:
        print_warn(f"No note found with ID: {note_id} or title: {title}")
        return
        
    clear_terminal()
    display_note(note, width=width, footer=True)


@note.command()
@click.argument('note_id', required=False)
@click.option("--width", type=int, default=50, help="Set the width for displaying the note")
def edit(note_id, width):
    """Edit a note (last edited if none specified)."""
    with SessionLocal() as session:
        handle_edit_note(session, note_id, width=width)

@note.command()
@click.argument('note_id')
def archive(note_id):
    """Archive (soft delete) a note."""
    note = Note.read(note_id)
    note.meta.archive()
    note.persist()

@note.command()
@click.argument('note_id')
def remove(note_id):
    """Permanently removes a note."""
    note = Note.read(note_id)
    if note:
        note.remove()

@note.command()
@click.argument('note_id')
def export(note_id):
    """Export note via LLM generate.""" # TODO makes sense?
    print(Note.read(note_id).dumps())

@note.command()
@click.option('--tag', '-t', multiple=True, help="Filter by tags")
@click.option('--entity', '-e', multiple=True, help="Filter by entities")
@click.option('--content', '-c', multiple=True, help="Filter by content")
@click.option('--limit', type=int, default=10, help="Limit the number of notes displayed.")
@click.option('--all', is_flag=True, help="List all notes including archived.")
@click.option('--archived', is_flag=True, help="List archived notes.")
def list(*args, **kwargs):
    """Lists notes based on provided filters (tags, entities, or content)."""

    # Get the current workspace
    ws = Workspace.get()

    # Read note files # TODO return more than just names...
    # notes = ws.list_notes()

    # if not notes:
    #     print_warn("No notes found.")
    #     return
    
    try:
        index_df = ws.get_index()
    except FileNotFoundError:
        print_warn("Index file not found.")
        return
    
    print(tabulate(index_df, headers='keys', tablefmt='psql'))
    
    # headers = [fsys("ID"), fsys("Title"), fsys("Snippets"), fsys("Created At"), fsys("Tags"), fsys("Entities"), fsys("Times")]
    # table = [
    #     [
    #         fsys(note), # ID... TODO
    #         "", #note.title,
    #         "", #note.size,
    #         "", #note.getCreatedAt(),
    #         "", #", ".join([ftag(tag) for tag in note.tags]),
    #         "", #", ".join([fentity(entity) for entity in note.entities]),
    #         "", # ", ".join([f"{t.literal}" for t in note.timesAll])
    #     ]
    #     for note in notes
    # ]
    # table = [
    #     [
    #         fsys(note_id),
    #         note["Title"],
    #         note["Snippets"],
    #         note["Created At"],
    #         ", ".join([ftag(tag) for tag in note["Tags"]]),
    #         ", ".join([fentity(entity) for entity in note["Entities"]]),
    #         ", ".join([f"{t.literal}" for t in note["Times"]])
    #     ]
    #     for note_id, note in index_df.iterrows()
    # ]


    # click.echo(tabulate(table, headers=headers, tablefmt="simple_outline"))