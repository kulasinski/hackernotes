import click

from . import hn

# === Graph Commands ===
@hn.group()
def graph():
    """Graph operations."""
    pass

@graph.command()
def show():
    pass

@graph.command()
def extend():
    pass

@graph.command()
@click.argument('note_id')
def place(note_id):
    pass