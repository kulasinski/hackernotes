import click

from . import hn

# === Workspace Commands ===
@hn.group()
def workspace():
    """Workspace management."""
    pass

@workspace.command()
@click.argument('name')
def new(name):
    pass

@workspace.command()
@click.argument('id')
def switch(id):
    pass

@workspace.command()
def config():
    pass

@workspace.command()
@click.argument('id')
def delete(id):
    pass