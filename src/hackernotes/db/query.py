# hackernotes/db/query.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from datetime import datetime
from uuid import uuid4
from typing import Optional, List, Set

from hackernotes.utils.term import print_sys, print_warn

from .models import Entity, Note, Snippet, Tag, TimeExpr, User, Workspace
from ..utils.config import config

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
        snippets: List[dict],
    ) -> Note:
        note = Note(
            id=str(uuid4()),
            workspace_id=workspace_id,
            title=title,
        )

        session.add(note)
        session.flush()  # get note.id before inserting snippets

        for i, snippet_kwargs in enumerate(snippets):
            SnippetCRUD.create(
                session,
                note_id=note.id,
                position=i,
                **snippet_kwargs
            )

        session.commit()
        return note

    @classmethod
    def get(cls, session: Session, note_id: str = None, title: str = None) -> Optional[Note]: #TODO add fetch security -- what about workspace id? not needed because user is quite specific!
        """
        Get a note by ID or title. If both are provided, ID takes precedence.
        """

        # Basic query
        stmt = select(Note)\
            .options(
                joinedload(Note.snippets),  # Eagerly load snippets
                joinedload(Note.snippets, Snippet.tags),  # Eagerly load snippet tags
                joinedload(Note.snippets, Snippet.entities),  # Eagerly load snippet entities
                joinedload(Note.snippets, Snippet.time_exprs),  # Eagerly load snippet time expressions
            )\
            .limit(1)
        
        if note_id is None and title is None:
            print_sys("No note ID or title provided. Returning last edited note.")
            stmt = stmt.order_by(Note.updated_at.desc())
            
        elif note_id is not None:
            stmt = stmt.where(Note.id == note_id)

        elif title is not None:
            stmt = stmt.where(Note.title == title)
            
        else:
            raise ValueError("Weird... this should not happen. Please check the code.")

        return session.execute(stmt).unique().scalars().one_or_none()

    @classmethod
    def list_by_workspace(cls, session: Session, workspace_name: str = config["active_workspace"], **filters) -> List[Note]:
        # Get workspace ID from name
        workspace_id = WorkspaceCRUD.get(session, workspace_name=workspace_name).id
        if not workspace_id:
            raise ValueError(f"Workspace `{workspace_name}` not found.")
        
        print_sys(f"Listing notes for workspace: {workspace_name} ({workspace_id}) with filters {filters}")

        # Prepare the base query - eager join
        stmt = select(Note)\
            .where(Note.workspace_id == workspace_id)\
            .options(
                joinedload(Note.snippets),  # Eagerly load snippets
                joinedload(Note.snippets, Snippet.tags),  # Eagerly load snippet tags
                joinedload(Note.snippets, Snippet.entities),  # Eagerly load snippet entities
                joinedload(Note.snippets, Snippet.time_exprs),  # Eagerly load snippet time expressions
            )
        
        # Handle archived and active notes
        if filters.get("archived", False): # list only archived notes when `archived` is specified
            # print_sys(f"Listing archived notes for workspace: {workspace_name} ({workspace_id})")
            stmt = stmt.where(Note.archived == True)
        elif not filters.get("all", False): # list only active = non-archived notes when `all` is not specified
            # print_sys(f"Listing active notes for workspace: {workspace_name} ({workspace_id})")
            stmt = stmt.where(Note.archived == False)

        # Handle tags
        tags = filters.get("tag", None)
        if tags:
            for tag in tags:
                stmt = stmt.join(Note.snippets).join(Snippet.tags).where(Tag.name.in_(tags))

        # Handle entities
        entities = filters.get("entity", None)
        if entities:
            for entity in entities:
                stmt = stmt.join(Note.snippets).join(Snippet.entities).where(Entity.name.in_(entities))

        # Handle content
        content = filters.get("content", None)
        if content:
            for c in content:
                stmt = stmt.where(Note.snippets.any(Snippet.content.ilike(f"%{c}%")))


        # Handle limit
        limit = filters.get("limit", None)
        if limit:
            stmt = stmt.limit(limit)
        else:
            print_warn(f"WARNING: Listing ALL notes in workspace. Please provide a limit or filters for better results.")

        # Handle order
        stmt.order_by(Note.updated_at.desc())

        return session.execute(stmt).unique().scalars().all()

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
        note.updated_at = datetime.now()
        session.commit()
        return True
    
class SnippetCRUD:
    @classmethod
    def create(
        cls,
        session: Session,
        note_id: str = None,
        content: str = None,
        position: Optional[int] = None,
        tags: Optional[Set[str]] = None,
        entities: Optional[Set[str]] = None,
        times: Optional[List[dict]] = None,
        annotations_only: Optional[bool] = False,
    ) -> Snippet:
        
        if note_id is None:
            raise ValueError("Note ID must be provided.")
        if content is None:
            raise ValueError("Snippet content must be provided.")
        
        snippet = Snippet(
            id=str(uuid4()),
            note_id=note_id,
            content=content,
            position=position,
            annotations_only=annotations_only,
        )

        if tags:
            for tag_name in tags:
                tag = session.get(Tag, tag_name) or Tag(name=tag_name)
                snippet.tags.append(tag)

        if entities:
            for entity_name in entities:
                entity = session.get(Entity, entity_name) or Entity(name=entity_name)
                snippet.entities.append(entity)

        if times: # TODO
            for time_kwargs in times:
                time_expr = TimeExpr(**time_kwargs)
                snippet.time_exprs.append(time_expr)

        session.add(snippet)
        session.commit()
        return snippet