import click

from . import hn

# === Annotation Commands ===

# --- Tag Commands ---

@hn.group()
def tag():
    pass

@tag.command()
@click.option('--used', is_flag=True)
def list(used):
    pass

# --- Entity Commands ---

@hn.group()
def entity():
    pass

@entity.command()
@click.option('--used', is_flag=True)
def list(used):
    pass

# --- Time Commands ---v

@hn.group()
def time():
    pass

@time.command()
@click.option('--used', is_flag=True)
def list(used):
    pass