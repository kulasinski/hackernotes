from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel

from ...utils.datetime import dt_dumps, dt_loads

class NoteMeta(BaseModel):
    """Note metadata model."""
    id: str = uuid4().hex
    title: str = "Untitled"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    archived: bool = False

    def touch(self):
        """Updates the updated_at timestamp."""
        self.updated_at = datetime.now()

    def archive(self):
        """Archives the note."""
        self.archived = True
        self.touch()

    # --- Serialization Methods ---
    def dumps(self) -> str:
        """Serialize the note metadata to a string."""
        data = f"[ID]: {self.id}\n"
        data += f"[TITLE]: {self.title}\n"
        data += f"[CREATED_AT]: {dt_dumps(self.created_at)}\n"
        data += f"[UPDATED_AT]: {dt_dumps(self.updated_at)}\n"
        data += f"[ARCHIVED]: {self.archived}\n"
        return data
    
    @classmethod
    def loads(cls, content: str) -> "NoteMeta":
        """Deserialize the note metadata from a string."""
        import re
        lines = content.strip().split("\n")
        data = {}
        for line in lines:
            # use regex
            match = re.match(r"\[(.*?)\]: (.*)", line)
            if not match:
                continue
            key, value = match.groups()
            key = key.strip()
            value = value.strip()
            if key == "[ID]":
                data["id"] = value
            elif key == "[TITLE]":
                data["title"] = value
            elif key == "[CREATED_AT]":
                data["created_at"] = dt_loads(value)
            elif key == "[UPDATED_AT]":
                data["updated_at"] = dt_loads(value)
            elif key == "[ARCHIVED]":
                data["archived"] = value.lower() == "true"
            else:
                raise ValueError(f"Unknown key: {key}")
        # Check if all required fields are present
        required_fields = ["id", "title", "created_at", "updated_at", "archived"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        return NoteMeta(**data)


        