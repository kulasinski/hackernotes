import click

from . import hn

# === Aliases ===
@hn.command(name="show")
@click.argument('note_id', required=False)
def show_alias(note_id):
    pass
    # show.invoke(click.Context(show), note_id=note_id)

@hn.command(name="new")
@click.argument('title', required=False)
def new_alias(title):
    pass
    # new.invoke(click.Context(new), title=title)

@hn.command(name="list")
@click.option('--all', is_flag=True)
def list_alias(all):
    pass
    # list.invoke(click.Context(list), all=all)