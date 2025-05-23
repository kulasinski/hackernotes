import click

from hackernotes.core.note import Note

from . import hn
from ..utils.term import clear_previous_line, fsys, print_warn, print_sys, print_err
from ..utils.config import config
from ..core.workspace import Workspace

# === Workspace Commands ===
@hn.group()
def ws():
    f"""Workspace management."""

@ws.command()
def active():
    """
    Show the active workspace.
    """
    print(fsys("Active workspace:"), config.get('active_workspace'))

@ws.command()
@click.argument('name')
@click.option('--description', '-d', default='', help='Description of the workspace')
def create(name, description):
    """
    Create a new workspace with the given name.
    """
    Workspace.create(name=name, description=description)

@ws.command()
@click.argument('name')
def use(name):
    """
    Use a workspace by name.
    """
    Workspace.use(name)

@ws.command()
def list():
    """
    List all workspaces.
    """
    workspaces = Workspace.list()
    if not workspaces:
        print_warn("No workspaces found.")
        return
    print_sys("Available workspaces:")
    for ws in workspaces:
        print(fsys(" -"),ws)

@ws.command()
@click.argument('name')
@click.option('--description', '-d', default=None, help='New description of the workspace')
@click.option('--new-name', '-n', default=None, help='New name for the workspace')
def update(name, description, new_name):
    """
    Update a workspace's name or description.
    """
    ws = Workspace.get(name)
    if ws is None:
        return
    
    ws.update(description=description, name=new_name)

@ws.command()
@click.argument('name')
def remove(name):
    """
    Remove a workspace by name.
    """
    Workspace.get(name).remove()

@ws.command()
@click.argument('note_id', required=False)
def index(note_id):
    """
    Index a note by ID. If no ID is provided, index all notes in the workspace.
    """
    if note_id:
        Note.index(note_id)
    else:
        print_sys("Indexing all notes in the workspace...")
        Note.index_all()
        clear_previous_line()
    print_sys("Indexing complete.")