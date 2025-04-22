

import signal
import sys
from hackernotes.core.note import NoteService
from hackernotes.db.models import Note
from hackernotes.db.query import NoteCRUD, WorkspaceCRUD
from hackernotes.utils.term import clear_terminal, print_sys, print_warn


def handle_create_note(session, title: str):
    """
    Handle the interactive creation of a new note.
    """

    # Get current workspace
    ws = WorkspaceCRUD.get_current(session)

    # Start...
    clear_terminal()
    print_sys(f"New note: {title}")
    print_sys("Enter snippets one by one. (Ctrl+D to save note, Ctrl+C to discard note):")
    note = NoteCRUD.create(
        session, 
        ws.id,
        title=title,
        snippets=[],
    )

    # Define signal handlers
    def handle_interrupt(sig, frame):
        print_warn("\nCancelling and deleting note...")
        NoteCRUD.delete(session, note.id, confirm=False)  # Deleting the note on Ctrl+C
        sys.exit(0)
    
    signal.signal(signal.SIGINT, handle_interrupt)

    NoteService(note).interactive_create(session)
    
    