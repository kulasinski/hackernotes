# hackernotes/db/query.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from uuid import uuid4
from typing import Optional, List, Set

from .models import Entity, Note, Snippet, Tag, TimeExpr, User, Workspace

class WorkspaceCRUD:
    @classmethod
    def create(cls, session: Session, user_id: str, name: str, model_backend: str, model_config: Optional[str] = None) -> Workspace:
        ws = Workspace(
            id=str(uuid4()),
            user_id=user_id,
            name=name,
            model_backend=model_backend,
            model_config=model_config,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(ws)
        session.commit()
        return ws

    @classmethod
    def get(cls, session: Session, workspace_id: str = None, workspace_name: str = None) -> Optional[Workspace]:
        """
        Get a workspace by ID or name. If both are provided, ID takes precedence.
        """
        if workspace_id is None and workspace_name is None:
            raise ValueError("Either workspace_id or workspace_name must be provided.")
        if workspace_id is not None:
            return session.get(Workspace, workspace_id)
        if workspace_name is not None:
            stmt = select(Workspace).where(Workspace.name == workspace_name)
            return session.execute(stmt).scalars().one_or_none()
        return None

    @classmethod
    def list_by_user(cls, session: Session, user_id: str) -> List[Workspace]:
        """
        List all workspaces for a given user.
        """
        stmt = select(Workspace).where(Workspace.user_id == user_id).order_by(Workspace.created_at.asc())
        return session.execute(stmt).scalars().all()

    @classmethod
    def delete(cls, session: Session, workspace_id: str) -> bool:
        ws = cls.get(session, workspace_id)
        if not ws:
            return False
        session.delete(ws)
        session.commit()
        return True

    @classmethod
    def update_model_config(cls, session: Session, workspace_id: str, model_backend: str, model_config: Optional[str]) -> bool:
        """
        Update the model configuration for a workspace. 
        """
        ws = cls.get(session, workspace_id)
        if not ws:
            return False
        ws.model_backend = model_backend
        ws.model_config = model_config
        ws.updated_at = datetime.now()
        session.commit()
        return True
    
class UserCRUD:
    @classmethod
    def get(cls, session: Session, user_id: str) -> Optional[User]:
        """
        Get a user by ID.
        """
        return session.get(User, user_id)
    
    @classmethod
    def create(cls, session: Session, name: str, user_id: str = None) -> User:
        # TODO not the best logic...
        if not user_id:
            user_id = str(uuid4())
        user = User(
            id=user_id,
            name=name
        )
        session.add(user)
        session.commit()
        return user
    
class NoteCRUD:
    @classmethod
    def create(
        cls,
        session: Session,
        workspace_id: str,
        title: Optional[str],
        snippets: List[str],
        tags: Optional[Set[str]] = None,
        entities: Optional[Set[str]] = None,
        times: Optional[List[tuple]] = None,  # list of (literal, scope)
    ) -> Note:
        note = Note(
            id=str(uuid4()),
            workspace_id=workspace_id,
            title=title,
        )

        if tags:
            for tag_name in tags:
                tag = session.get(Tag, tag_name) or Tag(name=tag_name)
                note.tags.append(tag)

        if entities:
            for entity_name in entities:
                entity = session.get(Entity, entity_name) or Entity(name=entity_name)
                note.entities.append(entity)

        if times: # TODO
            for literal, scope in times:
                time_expr = TimeExpr(
                    value=f"{literal}-{scope}", literal=literal, scope=scope
                )
                note.time_exprs.append(time_expr)

        session.add(note)
        session.flush()  # get note.id before inserting snippets

        for i, content in enumerate(snippets):
            snippet = Snippet(
                id=str(uuid4()),
                note_id=note.id,
                content=content,
                position=i,
            )
            session.add(snippet)

        session.commit()
        return note

    @classmethod
    def get(cls, session: Session, note_id: str) -> Optional[Note]:
        return session.get(Note, note_id)

    @classmethod
    def list_by_workspace(cls, session: Session, workspace_id: str) -> List[Note]:
        stmt = select(Note).where(Note.workspace_id == workspace_id).order_by(Note.updated_at.desc())
        return session.execute(stmt).scalars().all()

    @classmethod
    def delete(cls, session: Session, note_id: str) -> bool:
        note = cls.get(session, note_id)
        if not note:
            return False
        session.delete(note)
        session.commit()
        return True

    @classmethod
    def archive(cls, session: Session, note_id: str) -> bool:
        note = cls.get(session, note_id)
        if not note:
            return False
        note.archived = True
        note.updated_at = datetime.utcnow()
        session.commit()
        return True