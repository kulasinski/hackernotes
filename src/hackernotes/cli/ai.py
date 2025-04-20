import click

from . import hn

# === AI/LLM Commands ===
@hn.group()
def llm():
    """LLM operations and task management."""
    pass

@llm.command()
def queue():
    pass

@llm.command()
def run():
    pass

@llm.command()
@click.argument('type')
def prompt(type):
    pass

@llm.command()
def chat():
    pass

@llm.command()
@click.argument('note_id')
def generate(note_id):
    pass