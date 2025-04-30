# core/note.py

from datetime import datetime
import signal
import sys
import os
from uuid import uuid4
from typing import Optional, List, Set

import click
from colorama import Fore, Style
from pydantic import BaseModel
from sqlalchemy.orm import Session
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import HTML

# this module is deprecated
raise ImportError("This module is deprecated. Use the new note system.")

class NoteService():
    def __init__(self, note: Note):
        self.note = note
        self.snippets: List[SnippetDB] = sorted(note.snippets, key=lambda x: x.position)

    @property
    def id(self) -> str:
        return self.note.id

    @property
    def title(self) -> str:
        return self.note.title

    @property
    def size(self) -> int:
        return len(self.note.snippets)

    @property
    def tags(self) -> Set[str]:
        tags = set()
        for snippet in self.note.snippets:
            for tag in snippet.tags:
                tags.add(tag.name)
        return tags
    
    @property
    def entities(self) -> Set[str]:
        entities = set()
        for snippet in self.note.snippets:
            for entity in snippet.entities:
                entities.add(entity.name)
        return entities
    
    @property
    def times(self):
        raise NotImplementedError("Times property is not implemented yet.")
    
    def getCreatedAt(self, format: str = dateFormat) -> datetime|str:
        if format:
            return self.note.created_at.strftime(format)
        return self.note.created_at
    
    def getUpdatedAt(self, format: str = dateFormat) -> datetime|str:
        if format:
            return self.note.updated_at.strftime(format)
        return self.note.updated_at
    
    @staticmethod
    def displaySnippet(snippet: SnippetDB):
        snippet_content = snippet.content
        # Highlight tags and entities
        for tag in snippet.tags:
            snippet_content = snippet_content.replace(f"#{tag.name}", f"{Fore.GREEN}#{tag.name}{Style.RESET_ALL}")
        for entity in snippet.entities:
            snippet_content = snippet_content.replace(f"@{entity.name}", f"{Fore.MAGENTA}@{entity.name}{Style.RESET_ALL}")
        
        # Highlight times # TODO !!!

        # Highlight URLs # TODO ???
        # for url in snippet.urls:
        #     snippet_content = snippet_content.replace(url, f"{Fore.LIGHTBLACK_EX}{url}{Style.RESET_ALL}")
        # Display snippet
        print(f"{Fore.CYAN}[{snippet.position}]{Style.RESET_ALL} {snippet_content}")
    
    def display(self, width: int = 80, footer: bool = True):
        """Displays the note in a formatted way."""
        print("\n"+"=" * width)
        print(fsys("Note title: ")+self.title)
        print(fsys(f"Created at: {self.getCreatedAt()}"))
        print("-" * width)

        # (Re)-order snippets by position
        self.snippets = sorted(self.snippets, key=lambda x: x.position)

        # Display snippets
        for snippet in self.snippets:
            NoteService.displaySnippet(snippet)
            
        if footer:
            print("-" * width)
            if self.entities:
                print(fsys("Entities: ")+', '.join([fentity(e) for e in self.entities]))
            if self.tags:
                print(fsys("Tags: ")+', '.join([ftag(tag) for tag in self.tags]))
            # if self.timesAll: # TODO 
            #     print(fsys("Times: ")+', '.join([f"{time.literal} ({time.scope})" for time in self.timesAll]))
            # if self.urls: # TODO ??
            #     print(fsys("URLs: ")+', '.join([f"{Fore.LIGHTBLACK_EX}{url.value}{Style.RESET_ALL}" for url in self.urls]))

            print("=" * width + "\n")

    def snippet_add(self, session, content: str, display: bool=False) -> Optional[SnippetDB]:
        """Adds a snippet to a note and DB and extracts tags/entities."""

        # Extract tags, entities, and URLs
        tags, entities = extract_tags_and_entities(content) # TODO
        times = [] # TODO
        # urls = extract_urls(content) # TODO ???

        # check if snippet is composed of tags only. If so, do not add a snippet, instead add tags to note
        # DEPRECATED
        # if containsTagsOnly(content):
        #     if display:
        #         clear_terminal_line()
        #     self.tags.update(tags)
        #     self.persist(db=db)
        #     print(f"{Fore.CYAN}✅ Tags {tags} added to current note{Style.RESET_ALL}")
        #     return None

        # Create snippet object (+persist)
        snippet = SnippetCRUD.create(
            session,
            note_id=self.id,
            content=content,
            position=len(self.snippets),
            tags=tags,
            entities=entities,
            times=times,
            annotations_only=False # TODO
        )

        if not snippet:
            print_err(f"❌ Failed to create snippet")
            return None
        
        # Add snippet to the instance
        self.snippets.append(snippet)

        if display:
            # clear_terminal_line()
            cursor_up()
            NoteService.displaySnippet(snippet)
            # snippet.display(ord=len(self.snippets)+1)

        return snippet

    def snippet_delete(self, session: Session, snippet_idx: int):
        if snippet_idx < 0 or snippet_idx > (len(self.snippets)-1):
            print_err(f"❌ Invalid snippet number: {snippet_idx}")
            return False

        # Get the snippet to delete
        snippet = self.snippets[snippet_idx]
        
        # Delete from database
        SnippetCRUD.delete(session, snippet.id)
        
        # Remove from local list
        self.snippets.pop(snippet_idx)
        
        # Reorder remaining snippets
        for i, s in enumerate(self.snippets):
            if s.position != i:
                s.position = i
                SnippetCRUD.update(session, s.id, position=i)
        
        # Clear and redisplay the note
        # clear_terminal()
        # self.display(footer=False)
        
        return True
        
    def interactive_create(self, session):
        """Interactive input for note creation or update."""

        def handle_exit(sig, frame):
            clear_terminal_line()
            # self.to_queue() # TODO
            print_sys(f"[+] Note {self.id} saved and added to the queue.")
            sys.exit(0)

        signal.signal(signal.SIGQUIT, handle_exit)

        # Create a prompt session with history
        prompt_session = PromptSession(history=InMemoryHistory())

        # Loop to accept multiple snippets from the user
        marked_for_reinput = False # Flag to reinput the current snippet
        while True:
            try:
                content = click.prompt(fsys(">>>"), prompt_suffix="")
            except click.Abort:
                handle_exit(None, None)
            if not content.strip():
                continue

            # --- Check for special commands --- # TODO let the user know about those special commands

            # --- Exit ---
            if content in ["/exit", "/quit", "/q"]:
                handle_exit(None, None)
            # --- Delete snippet ---
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
                NoteCRUD.archive(session, self.id)
                break
            # --- Edit snippet ---
            elif content.startswith("/edit") or content.startswith("/e"):
                # --- Edit snippet ---
                snippet_ord = int(content.split()[1])
                if snippet_ord < 0 or snippet_ord > (len(self.snippets)-1):
                    print_err(f"❌ Invalid snippet number: {snippet_ord}")
                    continue
                # Get the snippet to edit
                snippet = self.snippets[snippet_ord]

                # Use prompt_toolkit to edit with the original content pre-filled
                new_content = prompt_session.prompt(
                    HTML(f"<ansicyan>[{snippet_ord}] (edit):</ansicyan> "),
                    default=snippet.content
                )

                # Update and overwrite
                snippet = SnippetCRUD.update(session, snippet.id, content=new_content)
                # Update the local snippet list
                self.snippets[snippet_ord] = snippet
                marked_for_reinput = True
                break
            # --- Edit title ---
            elif content.startswith("/title"):
                if len(content.split(" ", 1)) < 2:
                    print_err(f"❌ No title provided. Use /title <new_title>")
                    continue
                title = ' '.join(content.split(" ", 1)[1:]).strip()
                # update the note title
                self.note.title = title
                NoteCRUD.update(session, self.id, title=title)
                marked_for_reinput = True
                break
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
                self.snippet_add(session, content, display=True)

        if marked_for_reinput:
            clear_terminal()
            self.display(footer=False)
            self.interactive_create(session)


