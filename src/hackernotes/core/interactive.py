

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

    # Create interactively
    NoteService(note).interactive_create(session)

def handle_edit_note(session, note_id: str, width: int = 50):
    """
    Handle the interactive editing of a note.
    """

    # Get note from database
    note = NoteCRUD.get(session, note_id=note_id)
    if not note:
        print_warn(f"Note with ID {note_id} not found.")
        return
    
    # clear_terminal()
    print_sys("Enter snippets one by one. (Ctrl+D to save note):")

    # Display the current note's state
    ns = NoteService(note)
    ns.display(width=width, footer=False)

    # Edit interactively
    ns.interactive_create(session)
    
    