import click

from hackernotes.utils.datetime import now

from . import hn
from .note import list as note_list
from .note import show as note_show
from .note import new as note_new
from .note import edit as note_edit
from .workspace import use as workspace_use

# === Aliases ===
@hn.command(name="show")
@click.argument('note_id', required=False)
@click.option("--title", type=str, help="Fetch by the note title")
@click.option("--width", type=int, default=50, help="Set the width for displaying the note")
def show_alias(*args, **kwargs):
    """Show a note (alias)."""
    ctx = click.Context(note_show)
    ctx.params = kwargs
    note_show.invoke(ctx)

@hn.command(name="new")
@click.argument('title', type=str, required=False, default=f'Untitled {now()}')
def new_alias(title):
    """Create a new note (alias)."""
    ctx = click.Context(note_new)
    ctx.params = {'title': title}
    note_new.invoke(ctx)

@hn.command(name="edit")
@click.argument('note_id', required=False)
@click.option("--width", type=int, default=50, help="Set the width for displaying the note")
def edit_alias(*args, **kwargs):
    """Edit a note (alias)."""
    ctx = click.Context(note_edit)
    ctx.params = kwargs
    note_edit.invoke(ctx)

@hn.command(name="list")
@click.option('--tag', '-t', multiple=True, help="Filter by tags")
@click.option('--entity', '-e', multiple=True, help="Filter by entities")
@click.option('--content', '-c', multiple=True, help="Filter by content")
@click.option('--limit', type=int, default=10, help="Limit the number of notes displayed.")
@click.option('--all', is_flag=True, help="List all notes including archived.")
@click.option('--archived', is_flag=True, help="List archived notes.")
def list_alias(*args, **kwargs):
    """List notes (alias)."""
    ctx = click.Context(note_list)
    ctx.params = kwargs
    note_list.invoke(ctx)

@hn.command()
@click.option('--name', help='Name of the workspace')
@click.option('--id', help='ID of the workspace')
def use(id: str = None, name: str = None): # TODO check
    workspace_use(id=id, name=name)