from datetime import datetime

from sqlalchemy import (
    Column, String, Text, JSON, Boolean, DateTime, ForeignKey, Integer, CheckConstraint
)
from sqlalchemy.orm import declarative_base

from ..core.types import (
    TaskStatus, PromptType, TimeScope
)

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    settings = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class Workspace(Base):
    __tablename__ = "workspace"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    model_backend = Column(String, nullable=False)
    model_config = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class Note(Base):
    __tablename__ = "note"
    id = Column(String, primary_key=True)
    workspace_id = Column(String, ForeignKey("workspace.id", ondelete="CASCADE"))
    title = Column(String, default="Untitled", nullable=False)
    archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Snippet(Base):
    __tablename__ = "snippet"
    id = Column(String, primary_key=True)
    note_id = Column(String, ForeignKey("note.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    position = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class Tag(Base):
    __tablename__ = "tag"
    name = Column(String, primary_key=True)

class Entity(Base):
    __tablename__ = "entity"
    name = Column(String, primary_key=True)
    entity_type = Column(String)

class TimeExpr(Base):
    __tablename__ = "time_expr"
    value = Column(String, primary_key=True)
    literal = Column(String, nullable=False)
    scope = Column(String, CheckConstraint(
        f"scope IN ({TimeScope.to_str()})"
    ))

class GraphNode(Base):
    __tablename__ = "graph_node"
    id = Column(String, primary_key=True)
    workspace_id = Column(String, ForeignKey("workspace.id", ondelete="CASCADE"))
    label = Column(String, nullable=False)
    parent_id = Column(String, ForeignKey("graph_node.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class GraphEdge(Base):
    __tablename__ = "graph_edge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(String, ForeignKey("graph_node.id"), nullable=False)
    target_id = Column(String, ForeignKey("graph_node.id"), nullable=False)

class Prompt(Base):
    __tablename__ = "prompt"
    id = Column(Integer, primary_key=True)
    workspace_id = Column(String, ForeignKey("workspace.id", ondelete="CASCADE"))
    prompt_type = Column(String, CheckConstraint(
        f"prompt_type IN ({PromptType.to_str()})"
    ))
    title = Column(String)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class AutomationQueue(Base):
    __tablename__ = "automation_queue"
    id = Column(Integer, primary_key=True)
    note_id = Column(String)
    snippet_id = Column(String)
    model_id = Column(String)
    task_type = Column(String, nullable=False)
    status = Column(String, CheckConstraint(
        f"status IN ({TaskStatus.to_str()})"
    ), default=TaskStatus.PENDING.name)
    status_detail = Column(Text)
    scheduled_at = Column(DateTime)
    executed_at = Column(DateTime)
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)