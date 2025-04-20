import os 

import click

from . import hn
from ..utils.config import CONFIG_DIR, DB_PATH
from ..utils.term import print_err, print_sys, input_sys

# === General ===
@hn.command()
@click.option('--db_path', default=DB_PATH, help="Path to the database file.")
def init(db_path: str):
    """Initialize HackerNotes for first-time use."""
    from ..db import init_db
    if os.path.exists(db_path):
        print_err(f"[!] Database already exists at {db_path}")
    else:
        init_db(db_path)

@hn.command()
def clean():
    """Cleanup or reset local state."""
    from ..db import delete_db
    # Add a confirmation prompt
    confirm = input_sys(f"Are you sure you want to delete the database at {DB_PATH}? (y/n): ")
    if confirm.lower() != 'y':
        print_err("Operation cancelled.")
        return
    delete_db()
    # TODO: Remove all local files??
    