# hackernotes/db/models.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: str
    name: Optional[str]
    email: Optional[str]
    settings: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class Workspace:
    id: str
    user_id: str
    name: str
    model_backend: str
    model_config: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class Note:
    id: str
    workspace_id: str
    title: Optional[str]
    archived: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class Snippet:
    id: str
    note_id: str
    content: str
    position: Optional[int]
    created_at: datetime
    updated_at: datetime

@dataclass
class Tag:
    name: str

@dataclass
class Entity:
    name: str
    entity_type: Optional[str]

@dataclass
class TimeExpr:
    value: str
    literal: str
    scope: str

@dataclass
class GraphNode:
    id: str
    workspace_id: str
    label: str
    parent_id: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class Prompt:
    id: int
    workspace_id: str
    prompt_type: str
    title: Optional[str]
    content: str
    created_at: datetime
    updated_at: datetime

@dataclass
class AutomationQueue:
    id: int
    note_id: Optional[str]
    snippet_id: Optional[str]
    model_id: Optional[str]
    task_type: str
    status: str
    status_detail: Optional[str]
    scheduled_at: Optional[datetime]
    executed_at: Optional[datetime]
    result: Optional[str]
    created_at: datetime
    updated_at: datetime
