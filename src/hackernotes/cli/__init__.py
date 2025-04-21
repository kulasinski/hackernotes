import os
import sys
import logging

import click

from ..utils.config import config, CONFIG_DIR, CONFIG_PATH
from ..utils.term import print_err, input_sys, print_sys
from ..db import delete_db

DB_PATH = config["db_path"]

def preflight():
    """ Pre-CLI Initialization Checks """
    if not os.path.exists(CONFIG_DIR):
        click.echo("[!] Configuration not initialized. Run 'hn init' first.")
        sys.exit(1)
    if not os.path.exists(DB_PATH):
        click.echo("[!] Database not found. Run 'hn init' to set up the environment.")
        sys.exit(1)
    click.echo("Preflight checks passed.")

@click.group()
def hn():
    """HackerNotes CLI (alias: hn)"""
    # click.echo("Welcome to HackerNotes CLI!")
    # preflight()
    pass

@hn.command()
def erase():
    """Erase all notes and settings."""

    confirm = input_sys(f"Are you sure you want to delete the HackerNotes along with all the data? This action cannot be undone (y/n): ")
    if confirm.lower() != 'y':
        print_err("Erase cancelled.")
        return
    
    # Delete the database file
    delete_db()

    # Delete the configuration directory
    if os.path.exists(CONFIG_DIR):
        os.remove(CONFIG_PATH)
        os.rmdir(CONFIG_DIR)
        print_sys(f"Configuration directory at {CONFIG_DIR} deleted.")
    else:
        print_err(f"No configuration directory found at {CONFIG_DIR}.")
