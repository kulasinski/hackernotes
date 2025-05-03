import signal
import sys

import click
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import ANSI, HTML

from hackernotes.utils.display import display_note, display_snippet

from .note import Note, NoteMeta
from ..utils.term import clear_terminal, clear_terminal_line, cursor_up, fsys, fwarn, print_err, print_sys, print_warn

def interactive_create(note: Note):
    """Interactive input for note creation or update."""

    def handle_exit(sig, frame):
        clear_terminal_line()
        note.persist()
        # note.to_queue() # TODO
        print_sys(fsys("[+] Note ")+note.meta.title+fsys(" saved and added to the queue."))
        note.index(note.meta.id)
        sys.exit(0)

    signal.signal(signal.SIGQUIT, handle_exit)

    # Create a prompt session with history
    prompt_session = PromptSession(history=InMemoryHistory())

    # Loop to accept multiple snippets from the user
    marked_for_reinput = False # Flag to reinput the current snippet
    while True:
        try:
            content = prompt_session.prompt(ANSI(fsys(">>> ")))
        except EOFError:
            handle_exit(None, None)
        if not content.strip():
            continue

        # --- Check for special commands --- # TODO let the user know about those special commands

        # --- Exit ---
        if content in ["/exit", "/quit", "/q"]:
            handle_exit(None, None)

        # --- Delete snippet --- TODO
        elif content.startswith("/delete ") or content.startswith("/d ") or content.startswith("/del "):
            # --- Delete snippet ---
            try:
                snippet_ord = int(content.split()[1])
            except (ValueError, IndexError):
                print_err(f"❌ Invalid snippet number: {content.split()[1]}")
                continue
            # Try to delete the snippet
            is_deleted = self.snippet_delete(session, snippet_ord)
            if is_deleted:
                # Reinput the current snippet and exit the current loop
                marked_for_reinput = True
                break
            else:
                # If deletion failed, continue the loop
                continue

        # --- Archive note ---
        elif content.startswith("/archive"):
            note.meta.archive()
            break

        # --- Edit snippet --- TODO
        elif content.startswith("/edit") or content.startswith("/e"):
            # --- Edit snippet ---
            snippet_ord = int(content.split()[1])
            if snippet_ord < 0 or snippet_ord > (note.snippets.length-1):
                print_err(f"❌ Invalid snippet number: {snippet_ord}")
                continue

            # Get the snippet to edit
            snippet = note.snippets[snippet_ord]

            # Use prompt_toolkit to edit with the original content pre-filled
            new_content = prompt_session.prompt(
                HTML(f"<ansicyan>[{snippet_ord}] (edit):</ansicyan> "),
                default=snippet.content
            )

            # Update and overwrite
            note.snippets.update(snippet_ord, new_content)

            marked_for_reinput = True
            break

        # --- Edit title ---
        elif content.startswith("/title"):
            if len(content.split(" ", 1)) < 2:
                print_err(f"❌ No title provided. Use /title <new_title>")
                continue
            title = ' '.join(content.split(" ", 1)[1:]).strip()
            # update the note title
            note.meta.title = title
            marked_for_reinput = True
            break

        # --- Add time ---
        # if content.startswith("/time"):
        #     # --- Add time ---
        #     literal = " ".join(content.split(" ", 1)[1:])
        #     self.add_time(literal, db=db)
        #     marked_for_reinput = True
        #     break

        # --- Print / commands ---
        elif content.startswith("/help") or content.strip() in ["/?","/h"]:
            print_sys(f"Available commands:")
            print_sys(f"  /exit, /quit, /q: Exit the note editor")
            print_sys(f"  /archive: Archive the note")
            print_sys(f"  /delete, /d, /del <snippet_ord>: Delete a snippet")
            print_sys(f"  /edit <snippet_ord>: Edit a snippet")
            print_sys(f"  /title: Edit the note title")
            print_sys(f"  /time <literal>: Add a time to the note")
            print_sys(f"  /help, /?, /h: Show this help message")
        
        else:
            note.add(content)
            cursor_up()
            display_snippet(note.snippets.length-1, note.snippets.last_snippet)

    if marked_for_reinput:
        clear_terminal()
        display_note(note, footer=False)
        interactive_create(note)

def handle_create_note(title: str):
    """
    Handle the interactive creation of a new note.
    """

    # Get current workspace
    # ws = WorkspaceCRUD.get_current(session)

    note = Note(
        meta=NoteMeta(
            title=title,
        )
    )

    clear_terminal()
    print_sys(f"New note: {title}")
    print_sys(f"ID: {note.meta.id}")
    print_sys("Enter snippets one by one. (Ctrl+D to save note, Ctrl+C to discard note):")

    # Define signal handlers
    def handle_interrupt(sig, frame):
        confirm = ""
        while confirm.lower() not in ['y', 'n']:
            confirm = input(fwarn("Do you want to discard the note? (y/n): "))
        if confirm.lower() == 'y':
            print_warn("Note discarded.")
            # note.remove(confirm=False) NOTE no need to remove the note as it is not persisted yet
        else:
            note.persist()
            print_sys("Note saved.")
            note.index(note.meta.id)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, handle_interrupt)

    # Create interactively
    # NoteService(note).interactive_create(session)

    try:
        interactive_create(note)
    except KeyboardInterrupt:
        # Handle Ctrl+C
        handle_interrupt(None, None)

def handle_edit_note(session, note_id: str, width: int = 50):
    """
    Handle the interactive editing of a note.
    """

    # Get note from database
    note = Note.read(note_id)
    if not note:
        print_warn(f"Note with ID {note_id} not found.")
        return
    
    # clear_terminal()
    print_sys("Enter snippets one by one. (Ctrl+D to save note):")

    # Display the current note's state
    display_note(note, width=width, footer=False)

    # Edit interactively
    interactive_create(note)
    
    