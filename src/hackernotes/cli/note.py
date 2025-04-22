from typing import List

import click
from tabulate import tabulate

from . import hn, preflight
from ..core.note import NoteService
from ..db import SessionLocal
from ..db.query import NoteCRUD
from ..utils.term import fentity, fsys, ftag

# === Note Commands ===
@hn.group()
def note():
    """Note-related operations."""
    preflight()

@note.command()
@click.argument('title', required=False)
def new(title):
    """Create new note with optional title."""
    pass

@note.command()
@click.argument('note_id', required=False)
@click.option("--width", type=int, default=50, help="Set the width for displaying the note")
def show(note_id):
    """Show a note (last edited if none specified)."""
    pass

@note.command()
@click.argument('note_id', required=False)
def edit(note_id):
    """Edit a note (last edited if none specified)."""
    pass

@note.command()
@click.argument('note_id')
def archive(note_id):
    """Archive (soft delete) a note."""
    pass

@note.command()
@click.argument('note_id')
def delete(note_id):
    """Permanently delete a note."""
    pass

@note.command()
@click.argument('note_id')
def export(note_id):
    """Export note via LLM generate."""
    pass

@note.command()
@click.option('--tag', '-t', multiple=True, help="Filter by tags")
@click.option('--entity', '-e', multiple=True, help="Filter by entities")
@click.option('--content', '-c', multiple=True, help="Filter by content")
@click.option('--limit', type=int, default=10, help="Limit the number of notes displayed.")
@click.option('--all', is_flag=True, help="List all notes including archived.")
@click.option('--archived', is_flag=True, help="List archived notes.")
def list(*args, **kwargs):
    """Lists notes based on provided filters (tags, entities, or content)."""

    with SessionLocal() as session:
        notes = [NoteService(n) for n in NoteCRUD.list_by_workspace(session, **kwargs)]

    if not notes:
        click.echo(f"No notes found.")
        return
    
    headers = [fsys("ID"), fsys("Title"), fsys("Snippets"), fsys("Created At"), fsys("Tags"), fsys("Entities"), fsys("Times")]
    table = [
        [
            fsys(note.id),
            note.title,
            note.size,
            note.getCreatedAt(),
            ", ".join([ftag(tag) for tag in note.tags]),
            ", ".join([fentity(entity) for entity in note.entities]),
            # ", ".join([f"{t.literal}" for t in note.timesAll])
            "Times not implemented"
        ]
        for note in notes
    ]

    click.echo(tabulate(table, headers=headers, tablefmt="simple_outline"))