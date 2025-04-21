import os

import click

from hackernotes.core.types import TimeScope

from . import hn
from ..db import init_db, SessionLocal
from ..db.query import NoteCRUD, UserCRUD, WorkspaceCRUD
from ..utils.config import config, update_config, CONFIG_DIR #DB_PATH, ACTIVE_WORKSPACE, MODEL_BACKEND
from ..utils.term import print_err, print_sys, input_sys

DB_PATH = config["db_path"]
ACTIVE_WORKSPACE = config["active_workspace"]
MODEL_BACKEND = config["model_backend"]

# === Initialization Commands ===
@hn.group()
@click.option('--db_path', default=DB_PATH, help="Path to the database file.")
def init(db_path: str):
    """Init operations."""
    pass

@init.command()
@click.option('--db_path', default=DB_PATH, help="Path to the database file.")
def db(db_path: str):
    pass

@hn.command(name="init") # TODO
@click.option('--db_path', default=DB_PATH, help="Path to the database file.")
@click.option('--username', default=os.getlogin(), help="User name")
@click.option('--workspace', default=ACTIVE_WORKSPACE, help="First and default workspace name")
def init_all(db_path: str, username: str, workspace: str):
    """Initialize HackerNotes for first-time use."""

    # Initialize DB
    init_db(db_path)

    with SessionLocal() as session:
        # Create user
        user = UserCRUD.create(session, name=username)
        print_sys(f"[+] Created user: {user.name} ({user.id})")

        # Create first workspace
        ws = WorkspaceCRUD.create(
            session,
            user_id=user.id,
            name=workspace,
            model_backend=MODEL_BACKEND,
            model_config=None
        )
        print_sys(f"[+] Created workspace: {ws.name} ({ws.id})")
        if workspace != ACTIVE_WORKSPACE:
            update_config(active_workspace=workspace)

        # Create first note
        initial_note = {
            "workspace_id": ws.id,
            "title": "Welcome to HackerNotes!",
            "snippets": [
                "This is your first note. You can edit it later, e.g. ^tomorrow.",
                "Use the `hackernotes` command to manage your notes. #protip",
                "I'm sure you are working on some @GrandVision !"
                "Happy hacking!"
            ],
            "tags": {"protip"},
            "entities": {"GrandVision"},
            "times": [
                ("tomorrow", TimeScope.DAY.value),
            ]
        }
        note = NoteCRUD.create(
            session,
            **initial_note,
        )
        print_sys(f"[+] Created initial note: {note.title} ({note.id})")
        print_sys(f"Initialization complete! Enjoy.")


    