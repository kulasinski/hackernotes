import click

from . import hn

# === Note Commands ===
@hn.group()
def note():
    """Note-related operations."""
    pass

@note.command()
@click.argument('title', required=False)
def new(title):
    """Create new note with optional title."""
    pass

@note.command()
@click.option('--all', is_flag=True, help="List all notes including archived.")
def list(all):
    """List notes."""
    pass

@note.command()
@click.argument('note_id', required=False)
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