# hackernotes/db/query.py
from datetime import datetime
from uuid import uuid4
from typing import Optional, List, Set

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, text
from tabulate import tabulate

from hackernotes.core.types import TimeIntelligence, EntityIntelligence
from hackernotes.utils.parsers import tags2line

from .models import Entity, Note, Snippet, Tag, TimeExpr, User, Workspace
from ..utils.config import config
from ..utils.term import fwarn, print_sys, print_warn

def execute_query(session: Session, query: str):
    """
    Execute a SQLAlchemy query and return the result.
    Print the output using tabulate.
    """
    try:
        # Ensure the query is wrapped in text() if it's a raw SQL string
        if isinstance(query, str):
            query = text(query)
        result = session.execute(query)
        if result.returns_rows:
            rows = result.fetchall()
            if rows:
                # Display using tabulate
                headers = result.keys()
                print_sys(tabulate(rows, headers=headers, tablefmt="grid"))
                return rows, headers
            else:
                print_sys("Query executed successfully. No rows returned.")
                return [], []
        else:
            print_sys("Query executed successfully. No rows returned.")
            return None, None
    except Exception as e:
        print_warn(f"Error executing query: {e}")
        raise e
        return None, None

class WorkspaceCRUD:
    @classmethod
    def create(cls, session: Session, user_id: str, name: str, model_backend: str, model_config: Optional[str] = None) -> Workspace:
        ws = Workspace(
            id=str(uuid4()),
            user_id=user_id,
            name=name,
            model_backend=model_backend,
            model_config=model_config,
        )
        session.add(ws)
        session.commit()
        return ws
    
    @classmethod
    def get_current(cls, session: Session) -> Optional[Workspace]:
        """
        Get the current workspace based on the active workspace name in the config.
        """
        active_workspace = config["active_workspace"]
        if not active_workspace:
            raise ValueError("No active workspace found in config.")
        
        stmt = select(Workspace).where(Workspace.name == active_workspace)
        return session.execute(stmt).scalars().one_or_none()

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
    def delete(cls, session: Session, note_id: str, confirm: bool = True) -> bool:
        note = cls.get(session, note_id)
        if not note:
            return False
        
        if confirm:
            confirmation = input(fwarn(f"Are you sure you want to delete note {note_id}? (y/n): "))
            if confirmation.lower() not in ["y", "yes"]:
                return None
            
        session.delete(note)
        session.commit()
        print_sys(f"Note {note_id} deleted.")
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
    
    @classmethod
    def update(
        cls,
        session: Session,
        note_id: str,
        title: Optional[str] = None,
        snippets: Optional[List[dict]] = None,
        tags: Optional[Set[str]] = None,
        entities: Optional[List[EntityIntelligence]] = None,
        times: Optional[List[TimeIntelligence]] = None,
    ) -> Note:
        
        note = cls.get(session, note_id)
        if not note:
            return None
        
        if title:
            note.title = title

        # TODO check
        # if snippets:
        #     for i, snippet_kwargs in enumerate(snippets):
        #         SnippetCRUD.create(
        #             session,
        #             note_id=note.id,
        #             position=i,
        #             **snippet_kwargs
        #         )

        if tags or entities or times:
            # TODO
            # 1. get all snippets content
            # 2. iterate over them and add tags (prepend #) where necessary
            # 3. create a new snippet with the remaining tags

            # iterate over all snippets
            all_existing_tags = set()
            all_existing_entities = set()
            for snippet in note.snippets:
                # get content
                content = snippet.content
                original_content = content
                # --- TAGS ---
                # get tags
                snippet_tags = {tag.name for tag in snippet.tags}
                all_existing_tags = all_existing_tags.union(snippet_tags)
                # iterate over tags
                added_tags = set()
                if tags:
                    for tag in tags:
                        # if the snippet does not have the tag yet and the tag is in the content, add it to the snippet
                        if tag not in snippet_tags and tag in content:
                            # add tag to snippet
                            content = content.replace(tag, f"#{tag}")
                            added_tags.add(tag)
                # --- ENTITIES ---
                snippet_entities = {EntityIntelligence(value=e.name, type=e.entity_type) for e in snippet.entities}
                all_existing_entities = all_existing_entities.union(snippet_entities)
                # iterate over entities
                if entities:
                    for entity in entities:
                        # if the snippet does not have the entity yet and the entity is in the content, add it to the snippet
                        if entity not in snippet_entities and entity.value in content:
                            # add entity to snippet
                            content = content.replace(entity.value, f"@{entity.value}:{entity.type.name}")
                            added_tags.add(entity.value)

                SnippetCRUD.update(
                        session,
                        snippet.id,
                        content=content,
                        tags=None if not added_tags else snippet_tags.union(added_tags), # add the new tags to the existing ones only if they are not None
                        entities=None if not added_tags else snippet_entities.union(added_tags), # add the new entities to the existing ones only if they are not None
                )
                # TODO entities
                # TODO times

                # TODO check if tags, entities or times are already present in the snippet
                # if not, add them to the snippet
            if tags:
                # add the remaining tags to the note
                remaining_tags = tags.difference(all_existing_tags)
                print(f"creating new snippet with tags: {remaining_tags}")
                # create a new snippet with the remaining tags
                content = f"Tag Intelligence: {tags2line(remaining_tags)}"
                SnippetCRUD.create(
                    session,
                    note_id=note.id,
                    content=content if original_content!=content else None, # only add the content if it is different from the original
                    position=len(note.snippets),
                    tags=set(remaining_tags),
                )


            # wrong
            # content = f"Tag Intelligence: {', '.join(['#' + tag for tag in tags])}"
            # SnippetCRUD.create(
            #     session,
            #     note_id=note.id,
            #     content=content,
            #     position=len(note.snippets),
            #     tags=set(tags),
            # )

        # if entities:
        #     for entity_name in entities:
        #         entity = session.get(Entity, entity_name) or Entity(name=entity_name)
        #         note.entities.append(entity)

        # session.commit()
        # print_sys(f"Note {note_id} updated.")
        # return note
    
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
    
    @classmethod
    def delete(cls, session: Session, snippet_id: str) -> bool:
        snippet = session.get(Snippet, snippet_id)
        if not snippet:
            return False
        session.delete(snippet)
        session.commit()
        return True
    
    @classmethod
    def update(
        cls,
        session: Session,
        snippet_id: str,
        content: Optional[str] = None,
        position: Optional[int] = None,
        tags: Optional[Set[str]] = None,
        entities: Optional[Set[str]] = None,
        times: Optional[List[dict]] = None,
    ) -> Snippet:
        if not any([content, position, tags, entities, times]):
            print_warn("No fields to update. Please provide at least one field.")
            return None
        print(f"Updating snippet {snippet_id} with content: {content}, position: {position}, tags: {tags}, entities: {entities}, times: {times}")
        return
        
        snippet = session.get(Snippet, snippet_id)
        if not snippet:
            return None
        
        if content:
            snippet.content = content
        if position:
            snippet.position = position

        if tags: # TODO check
            for tag_name in tags:
                tag = session.get(Tag, tag_name) or Tag(name=tag_name)
                snippet.tags.append(tag)

        if entities: # TODO check
            for entity_name in entities:
                entity = session.get(Entity, entity_name) or Entity(name=entity_name)
                snippet.entities.append(entity)

        if times: # TODO check
            for time_kwargs in times:
                time_expr = TimeExpr(**time_kwargs)
                snippet.time_exprs.append(time_expr)
        session.commit()
        return snippet