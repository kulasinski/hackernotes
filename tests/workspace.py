import os

from hackernotes.core.workspace import Workspace
from hackernotes.utils.config import WORKSPACES_DIR

def test_workspace_creation():
    # Test creating a new workspace
    ws = Workspace.create(name="test_workspace", description="This is a test workspace.")
    assert ws is not None
    assert ws.name == "test_workspace"
    assert ws.description == "This is a test workspace."
    assert ws.base_dir == os.path.join(WORKSPACES_DIR, "test_workspace")
    assert os.path.exists(ws.base_dir)
    assert os.path.exists(ws.file_path)

    # Test creating a workspace with invalid name
    invalid_ws = Workspace.create(name="invalid@workspace")
    assert invalid_ws is None

    # Test creating a workspace that already exists
    existing_ws = Workspace.create(name="test_workspace")
    assert existing_ws is None

    # Clean up
    ws.remove(confirm=False)

    # Check if cleanup was successful
    assert not os.path.exists(ws.base_dir)