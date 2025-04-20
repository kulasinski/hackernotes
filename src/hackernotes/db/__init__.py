# hackernotes/db/__init__.py

from .schema import SCHEMA_SQL
import sqlite3
import os

from ..utils.config import CONFIG_DIR, DB_PATH, update_config
from ..utils.term import print_sys

def get_connection(db_path: str = DB_PATH):
    """Get a connection to the SQLite database."""
    return sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)

def init_db(db_path: str = DB_PATH, db_suffix: str = ".db"):
    """Initialize the database and create tables if they don't exist."""
    # Add suffix to the database path if not already present
    if not db_path.endswith(db_suffix):
        db_path += db_suffix
    # Expand the user directory in the database path
    db_path = os.path.expanduser(db_path)

    # Check if the database file already exists
    if os.path.exists(db_path):
        print_sys(f"[!] Database already exists at {db_path}")
        return
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Initialize the database
    conn = get_connection(db_path=db_path)
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    print_sys(f"[+] Database initialized at {db_path}")

    # Update config
    if db_path != DB_PATH:
        update_config(db_path=db_path)

def db_exists():
    """Check if the database file exists."""
    return os.path.exists(DB_PATH)

def delete_db():
    """Delete the database file."""
    if db_exists():
        os.remove(DB_PATH)
        print_sys(f"[+] Deleted database at {DB_PATH}")
    else:
        print_sys(f"[!] No database found at {DB_PATH}")
