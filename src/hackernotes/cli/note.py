from typing import List
import click

from . import hn, preflight

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
@click.option('--all', is_flag=True, help="List all notes including archived.")
def list(all):
    """List notes."""
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
@click.option('--all', is_flag=True, help="List all notes including archived.")
# def list(tag: tuple[str, ...], entity: tuple[str, ...], content: tuple[str, ...], all: bool):
def list(*args, **kwargs):
    """Lists notes based on provided filters (tags, entities, or content)."""

    print("args:", args)
    print("kwargs:", kwargs)

    return

    notes = Note.search(filters)

    if not filters:
        click.echo(f"WARNING: Listing ALL {len(notes)} notes... Please provide at least one filter (tag, entity, or content) for better results.")
    else:
        click.echo(f"Found {len(notes)} notes matching filters: {filters}")

    if not notes:
        click.echo(f"No notes found matching filters: {filters}")
        return
    
    headers = [fsys("ID"), fsys("Title"), fsys("Snippets"), fsys("Created At"), fsys("Tags"), fsys("Entities"), fsys("Times")]
    table = [
        [
            fsys(str(note.id)),
            note.title,
            len(note.snippets),
            note.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            ", ".join([ftag(tag) for tag in note.tagsAll]),
            ", ".join([fentity(entity) for entity in note.entitiesAll]),
            ", ".join([f"{t.literal}" for t in note.timesAll])
        ]
        for note in notes
    ]

    click.echo(tabulate(table, headers=headers, tablefmt="simple_outline"))