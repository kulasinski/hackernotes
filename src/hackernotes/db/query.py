# hackernotes/db/query.py

import sqlite3
from typing import List, Optional
from . import get_connection
from .models import Note, Snippet
from datetime import datetime


def fetch_latest_note(conn: Optional[sqlite3.Connection] = None) -> Optional[Note]:
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    row = conn.execute(
        """
        SELECT id, workspace_id, title, archived, created_at, updated_at
        FROM note
        WHERE archived = 0
        ORDER BY updated_at DESC
        LIMIT 1
        """
    ).fetchone()

    if close_conn:
        conn.close()

    if row:
        return Note(*row)
    return None


def fetch_note_by_id(note_id: str, conn: Optional[sqlite3.Connection] = None) -> Optional[Note]:
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    row = conn.execute(
        """
        SELECT id, workspace_id, title, archived, created_at, updated_at
        FROM note WHERE id = ?
        """,
        (note_id,)
    ).fetchone()

    if close_conn:
        conn.close()

    if row:
        return Note(*row)
    return None


def fetch_snippets_for_note(note_id: str, conn: Optional[sqlite3.Connection] = None) -> List[Snippet]:
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    rows = conn.execute(
        """
        SELECT id, note_id, content, position, created_at, updated_at
        FROM snippet
        WHERE note_id = ?
        ORDER BY position ASC NULLS LAST, created_at ASC
        """,
        (note_id,)
    ).fetchall()

    if close_conn:
        conn.close()

    return [Snippet(*row) for row in rows]


def insert_note(note: Note, conn: Optional[sqlite3.Connection] = None):
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    conn.execute(
        """
        INSERT INTO note (id, workspace_id, title, archived, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (note.id, note.workspace_id, note.title, note.archived, note.created_at, note.updated_at)
    )
    conn.commit()
    if close_conn:
        conn.close()


def insert_snippet(snippet: Snippet, conn: Optional[sqlite3.Connection] = None):
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    conn.execute(
        """
        INSERT INTO snippet (id, note_id, content, position, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (snippet.id, snippet.note_id, snippet.content, snippet.position, snippet.created_at, snippet.updated_at)
    )
    conn.commit()
    if close_conn:
        conn.close()
