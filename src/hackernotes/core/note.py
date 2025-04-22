# core/note.py

from datetime import datetime
from uuid import uuid4
from typing import Optional, List, Set
from sqlalchemy.orm import Session

from ..db.models import Note, Snippet, Tag, Entity, TimeExpr
from ..utils.datetime import dateFormat

class NoteService():
    def __init__(self, note: Note):
        self.note = note

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
