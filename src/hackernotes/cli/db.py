import os 

import click
import readline

from . import hn
from ..db import SessionLocal
from ..db.query import execute_query
from ..utils.config import config
from ..utils.term import print_err, print_sys, input_sys, print_warn

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

@db.command()
@click.argument('query', type=str, required=False)
@click.option('--interactive', '-i', is_flag=True, help='Run in interactive mode.')
def exec(query: str, interactive: bool):
    """Execute a raw SQL query. Optionally run in interactive mode."""
    if query:
        with SessionLocal() as session:
            execute_query(session, query)
    elif interactive:
        print_sys("Running in interactive mode. Type 'exit' or 'q' or to quit.")
        historical_queries = []
        while True:
            try:
                query = input("SQL> ")  # Use input() to allow readline to work
                if query.lower() in ["exit", "q"]:
                    print_sys("Exiting interactive mode gracefully.")
                    break
                if query.strip():  # Add non-empty queries to history
                    historical_queries.append(query)
                    readline.add_history(query)
                with SessionLocal() as session:
                    execute_query(session, query)
            except KeyboardInterrupt:
                print_sys("\nExiting interactive mode gracefully.")
                break
            except Exception as e:
                print_err(f"Error: {e}")
    else:
        print_warn("No query provided. Use --interactive or -i to run in interactive mode.")
        return