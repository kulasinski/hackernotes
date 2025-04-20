import os
import sys
import logging

import click

from ..utils.config import CONFIG_DIR, DB_PATH

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