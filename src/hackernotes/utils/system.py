from pathlib import Path

HACKERNOTES_HEADER = "# Hackernotes {} file\n"

def path_contains_dir(root_path, target_dir_name):
    root = Path(root_path)
    return any(p.name == target_dir_name and p.is_dir() for p in root.rglob('*'))