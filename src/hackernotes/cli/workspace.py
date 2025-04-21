import click


from . import hn
from ..utils.term import print_err
from ..utils.config import update_config
from ..db.query import WorkspaceCRUD

# === Workspace Commands ===
@hn.group()
def workspace():
    """Workspace management."""
    pass

@workspace.command()
@click.argument('name')
def new(name):
    """
    Create a new workspace with the given name.
    """
    # Check if the workspace already exists
    ws = WorkspaceCRUD.get(workspace_name=name)
    if ws:
        print_err(f"Workspace '{name}' already exists.")
        return
    
    # Create the new workspace
    ws = WorkspaceCRUD.create(workspace_name=name)
    if ws:
        print(f"Workspace '{name}' created successfully.")
    else:
        print_err(f"Failed to create workspace '{name}'.")

@workspace.command()
@click.option('--name', help='Name of the workspace')
@click.option('--id', help='ID of the workspace')
def use(id: str = None, name: str = None):
    """
    Use a workspace by ID or name. If both are provided, ID takes precedence.
    """
    if id is None and name is None:
        print_err("Either workspace_id or workspace_name must be provided.")
        return
    
    # Check if the workspace exists
    ws = WorkspaceCRUD.get(id=id, name=name)
    if not ws:
        print_err(f"Workspace with ID '{id}' or name '{name}' does not exist.")
        return
    
    # Update the active workspace in the config
    update_config(active_workspace=ws.name)
    print(f"Now using workspace: {ws.name} (ID: {ws.id})")

@workspace.command()
def config():
    pass

@workspace.command()
@click.argument('id')
def delete(id):
    pass