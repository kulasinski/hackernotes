import os 

import click

from . import hn
from ..utils.config import config
from ..utils.term import print_err, print_sys, input_sys

DB_PATH = config["db_path"]

# === DB ===
@hn.group()
def db():
    """DB operations."""
    pass

@db.command(name="init")
@click.option('--db_path', default=DB_PATH, help="Path to the database file.")
def init(db_path: str):
    """Initialize HackerNotes database for first-time use."""
    from ..db import init_db
    init_db(db_path=db_path)

@db.command()
def remove():
    """Remove the database file."""
    from ..db import delete_db
    # Add a confirmation prompt
    confirm = input_sys(f"Are you sure you want to delete the database at {DB_PATH}? (y/n): ")
    if confirm.lower() != 'y':
        print_err("Operation cancelled.")
        return
    delete_db()
    # TODO: Remove all local files??