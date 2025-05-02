import os
from datetime import datetime
import shutil
import json
from typing import List

from pydantic import BaseModel, field_validator
import toml

from ..utils.system import path_contains_dir, HACKERNOTES_HEADER
from ..utils.term import fsys, print_err, print_sys, print_warn
from ..utils.config import WORKSPACES_DIR, config, update_config

class Workspace(BaseModel):
    """
    A workspace model that holds a collection of notes.
    Managements of: notes, annotations, LLMs, etc.
    """
    name: str
    description: str = ""
    created_at: datetime = datetime.now()

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        """
        Validates the workspace name.
        """
        # Check if name contains only alphanumeric characters, spaces, dashes, and underscores
        if not name.replace(" ", "").replace("-", "").replace("_", "").isalnum():
            raise ValueError(f"Workspace name '{name}' contains invalid characters. Only alphanumeric characters, spaces, dashes, and underscores are allowed.")
        return name

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
        # if not name.replace(" ", "").replace("-", "").replace("_", "").isalnum():
        #     print_err(f"Workspace name '{name}' contains invalid characters. Only alphanumeric characters, spaces, dashes, and underscores are allowed.")
        #     return None
        
        # Check if workspace already exists
        if path_contains_dir(WORKSPACES_DIR, name):
            print_err(f"Workspace '{name}' already exists.")
            return None
        
        # Create the workspace instance
        try:
            ws = cls(name=name, description=description)
        except ValueError as e:
            print_err(f"Failed to create workspace '{name}': {e}")
            return None

        # Create the workspace directory
        os.makedirs(ws.base_dir, exist_ok=False)

        # Create the workspace file
        ws.save()

        print_sys(f"[+] Created workspace '{name}' at {ws.base_dir}")
        
        # Create
        return cls(name=name, description=description)
    
    @classmethod
    def get(cls, name: str = config.get("active_workspace")) -> "Workspace":
        """
        Gets a workspace by name.
        Defaults to the active workspace.
        """
        if not cls.exists(name):
            print_err(f"Workspace '{name}' does not exist.")
            return None
        
        # Load the workspace file
        try:
            with open(os.path.join(WORKSPACES_DIR, name, f"__ws__.toml"), "r") as f:
                data = toml.load(f)
        except FileNotFoundError:
            print_err(f"Workspace file not found for '{name}'.")
            return None
        except toml.TomlDecodeError:
            print_err(f"Failed to decode workspace file for '{name}'.")
            return None
        
        try:
            # Validate the workspace data
            ws = cls.model_validate_json(json.dumps(data))
        except Exception as e:
            print_err(f"Failed to validate workspace data for '{name}': {e}")
            return None
        
        # Create the workspace instance
        return ws
    
    @classmethod
    def exists(cls, name: str) -> bool:
        """
        Checks if a workspace exists.
        """
        return os.path.exists(os.path.join(WORKSPACES_DIR, name))
    
    @classmethod
    def use(cls, name: str) -> "Workspace":
        """
        Uses a workspace by name.
        Checks if the workspace exists, updated the config's default, returns the workspace instance.
        """
        ws = cls.get(name)
        if ws is None:
            return None
        else:
            # Update the config's default/active workspace
            update_config(active_workspace=name)
            print_sys(f"[+] Now using workspace '{name}'")

        return ws
    
    @classmethod
    def list(cls) -> list[str]:
        """
        Lists all workspaces.
        """
        # Check if workspaces directory exists
        if not os.path.exists(WORKSPACES_DIR):
            print_err(f"Workspaces directory '{WORKSPACES_DIR}' does not exist. Create some workspace first.")
            return []
        # List all directories in the workspaces directory
        workspaces = [d for d in os.listdir(WORKSPACES_DIR) if os.path.isdir(os.path.join(WORKSPACES_DIR, d))]
        return workspaces
    
    @classmethod
    def get_or_create(cls, name: str, description: str = "") -> "Workspace":
        """
        Gets a workspace by name or creates it if it doesn't exist.
        """
        return cls.get(name) or cls.create(name, description)
    
    def list_notes(self, note_suffix: str = ".hnote") -> List[str]: # TODO this shouldn't be hardcoded, also return more than just names...
        """
        Lists all notes in the workspace.
        """
        # Check if the workspace directory exists
        if not os.path.exists(self.base_dir):
            print_err(f"Workspace '{self.name}' does not exist.")
            return []
        
        # List all files in the workspace directory, a note ends with suffix
        note_names = [f[:-len(note_suffix)] for f in os.listdir(self.base_dir)
                      if os.path.isfile(os.path.join(self.base_dir, f)) and f.endswith(note_suffix)]
        return note_names
    
    def save(self):
        """
        Saves the workspace to a file.
        """
        # Save the workspace file
        with open(self.file_path, "w") as f:
            f.write(HACKERNOTES_HEADER.format("WORKSPACE"))
            toml.dump(json.loads(self.model_dump_json()), f)
        
    def remove(self, confirm: bool = True):
        """
        Removes the workspace.
        """
        # Prevent removal if the workspace is active
        if self.name == config.get("active_workspace"):
            print_err(f"Cannot remove the active workspace '{self.name}'. Please switch to another workspace first.")
            return
        if confirm:
            # Add a confirmation prompt
            confirm = input(fsys("Are you sure you want to delete the workspace '{self.name}' at {self.base_dir}? (y/n): "))
            if confirm.lower() != 'y':
                print_err("Operation cancelled.")
                return

        # Remove the workspace directory
        shutil.rmtree(self.base_dir)
        print_warn(f"[+] Removed workspace '{self.name}' at {self.base_dir}")

    def update(self, name: str = None, description: str = None):
        """
        Updates the workspace.
        """
        if name:
            # Rename the workspace directory
            new_base_dir = os.path.join(WORKSPACES_DIR, name)
            os.rename(self.base_dir, new_base_dir)
            # Update the base_dir property
            self.name = name
        if description:
            self.description = description

        # Save the workspace file
        self.save()
        print_sys(f"[+] Updated workspace '{self.name}' at {self.base_dir}")