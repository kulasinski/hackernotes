# core/note.py

from datetime import datetime
import signal
import sys
from uuid import uuid4
from typing import Optional, List, Set

import click
from colorama import Fore, Style
from sqlalchemy.orm import Session

from ..db.query import NoteCRUD, SnippetCRUD
from ..db.models import Note, Snippet, Tag, Entity, TimeExpr
from ..utils.term import clear_terminal, clear_terminal_line, fentity, fsys, ftag, print_err, print_sys
from ..utils.datetime import dateFormat

class NoteService():
    def __init__(self, note: Note):
        self.note = note
        self.snippets: List[Snippet] = sorted(note.snippets, key=lambda x: x.position)

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
    def displaySnippet(snippet: Snippet):
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

    def add_snippet(self, session, content: str, display: bool=False) -> Optional[Snippet]:
        """Adds a snippet to a note and DB and extracts tags/entities."""

        # Extract tags, entities, and URLs
        tags, entities = {}, {} # extract_tags_and_entities(content) # TODO
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
            clear_terminal_line()
            NoteService.displaySnippet(snippet)
            # snippet.display(ord=len(self.snippets)+1)

        return snippet

    def interactive_create(self, session):
        """Interactive input for note creation or update."""

        def handle_exit(sig, frame):
            clear_terminal_line()
            # self.to_queue() # TODO
            print_sys(f"[+] Note {self.id} saved and added to the queue.")
            sys.exit(0)

        signal.signal(signal.SIGQUIT, handle_exit)

        # Loop to accept multiple snippets from the user
        marked_for_reinput = False # Flag to reinput the current snippet
        while True:
            try:
                content = click.prompt(fsys("> "), prompt_suffix="")
            except click.Abort:
                handle_exit(None, None)
            if not content.strip():
                continue

            # --- Check for special commands --- # TODO let the user know about those special commands
            if content in ["/exit", "/quit", "/q"]:
                # --- Exit ---
                handle_exit(None, None)
            # if content.startswith("/delete ") or content.startswith("/d ") or content.startswith("/del "):
            #     # --- Delete snippet ---
            #     snippet_ord = int(content.split()[1])
            #     self.handle_snippet_delete(snippet_ord=snippet_ord, db=db)
            #     # Reinput the current snippet and exit the current loop
            #     marked_for_reinput = True
            #     break
            if content.startswith("/archive"):
                NoteCRUD.archive(session, self.id)
                break
            # if content.startswith("/edit") or content.startswith("/e"):
            #     # --- Edit snippet ---
            #     snippet_ord = int(content.split()[1])
            #     snippet = self.snippets[snippet_ord-1]
            #     # Use `prompt` with a default value
            #     snippet.content = prompt(f"[{snippet_ord}] (edit): ", default=snippet.content)
            #     snippet.persist(note_id=self.id, db=db)
            #     marked_for_reinput = True
            #     break
            # if content == "/title":
            #     # --- Edit title ---
            #     self.title = prompt("Title (edit): ", default=self.title)
            #     self.persist(db=db)
            #     marked_for_reinput = True
            #     break
            # if content.startswith("/time"):
            #     # --- Add time ---
            #     literal = " ".join(content.split(" ", 1)[1:])
            #     self.add_time(literal, db=db)
            #     marked_for_reinput = True
            #     break
            self.add_snippet(session, content, display=True)

        if marked_for_reinput:
            clear_terminal()
            self.display(footer=False)
            self.interactive_create(session)
            
# class NoteService:
#     @staticmethod
#     def create_note(
#         session: Session,
#         workspace_id: str,
#         title: Optional[str],
#         snippet_contents: List[str],
#         tags: Optional[Set[str]] = None,
#         entities: Optional[Set[str]] = None,
#         times: Optional[List[tuple]] = None
#     ) -> Note:
#         note = Note(
#             id=str(uuid4()),
#             workspace_id=workspace_id,
#             title=title,
#             archived=False,
#             created_at=datetime.utcnow(),
#             updated_at=datetime.utcnow()
#         )

#         if tags:
#             for tag_name in tags:
#                 tag = session.get(Tag, tag_name) or Tag(name=tag_name)
#                 note.tags.append(tag)

#         if entities:
#             for entity_name in entities:
#                 entity = session.get(Entity, entity_name) or Entity(name=entity_name)
#                 note.entities.append(entity)

#         if times:
#             for literal, scope in times:
#                 time_expr = TimeExpr(
#                     value=f"{literal}-{scope}", literal=literal, scope=scope
#                 )
#                 note.time_exprs.append(time_expr)

#         session.add(note)
#         session.flush()

#         for i, content in enumerate(snippet_contents):
#             snippet = Snippet(
#                 id=str(uuid4()),
#                 note_id=note.id,
#                 content=content,
#                 position=i,
#                 created_at=datetime.utcnow(),
#                 updated_at=datetime.utcnow()
#             )
#             note.snippets.append(snippet)

#         session.commit()
#         return note

#     @staticmethod
#     def add_snippet(
#         session: Session,
#         note_id: str,
#         content: str,
#         position: Optional[int] = None,
#         tags: Optional[Set[str]] = None,
#         entities: Optional[Set[str]] = None,
#         times: Optional[List[tuple]] = None
#     ) -> Snippet:
#         snippet = Snippet(
#             id=str(uuid4()),
#             note_id=note_id,
#             content=content,
#             position=position,
#             created_at=datetime.utcnow(),
#             updated_at=datetime.utcnow()
#         )

#         if tags:
#             for tag_name in tags:
#                 tag = session.get(Tag, tag_name) or Tag(name=tag_name)
#                 snippet.tags.append(tag)

#         if entities:
#             for entity_name in entities:
#                 entity = session.get(Entity, entity_name) or Entity(name=entity_name)
#                 snippet.entities.append(entity)

#         if times:
#             for literal, scope in times:
#                 time_expr = TimeExpr(
#                     value=f"{literal}-{scope}", literal=literal, scope=scope
#                 )
#                 snippet.time_exprs.append(time_expr)

#         session.add(snippet)
#         session.commit()
#         return snippet
