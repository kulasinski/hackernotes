import click

from . import hn
from ..utils.term import fsys, print_warn, print_sys, print_err
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
def remove(name):
    """
    Remove a workspace by name.
    """
    Workspace.get(name).remove()