import os
from datetime import datetime

from pydantic import BaseModel
import toml

from ..utils.system import path_contains_dir, HACKERNOTES_HEADER
from ..utils.term import print_err, print_sys
from ..utils.config import WORKSPACES_DIR
import shutil

class Workspace(BaseModel):
    """
    A workspace model that holds a collection of notes.
    Managements of: notes, annotations, LLMs, etc.
    """
    name: str
    description: str = ""
    created_at: datetime = datetime.now()

    @property
    def base_dir(self) -> str:
        return os.path.join(WORKSPACES_DIR, self.name)
    
    @property
    def file_path(self) -> str:
        return os.path.join(self.base_dir, f"__ws__.toml")

    @classmethod
    def create(cls, name: str, description: str = "") -> "Workspace":
        """
        Creates a new workspace.
        """

        # Check if name contains only alphanumeric characters, spaces, dashes, and underscores
        if not name.replace(" ", "").replace("-", "").replace("_", "").isalnum():
            print_err(f"Workspace name '{name}' contains invalid characters. Only alphanumeric characters, spaces, dashes, and underscores are allowed.")
            return None
        
        # Check if workspace already exists
        if path_contains_dir(WORKSPACES_DIR, name):
            print_err(f"Workspace '{name}' already exists.")
            return None
        
        # Create the workspace instance
        ws = cls(name=name, description=description)

        # Create the workspace directory
        os.makedirs(ws.base_dir, exist_ok=False)

        # Create the workspace file
        with open(ws.file_path, "w") as f:
            f.write(HACKERNOTES_HEADER.format("WORKSPACE"))
            toml.dump(ws.model_json_schema(), f)

        print_sys(f"[+] Created workspace '{name}' at {ws.base_dir}")
        
        # Create
        return cls(name=name, description=description)
    
    def remove(self, confirm: bool = True):
        """
        Removes the workspace.
        """
        if confirm:
            # Add a confirmation prompt
            confirm = input(f"Are you sure you want to delete the workspace at {self.base_dir}? (y/n): ")
            if confirm.lower() != 'y':
                print_err("Operation cancelled.")
                return

        # Remove the workspace directory
        shutil.rmtree(self.base_dir)
        print_sys(f"[+] Removed workspace '{self.name}' at {self.base_dir}")