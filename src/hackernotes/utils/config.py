import os

import toml

from ..utils.term import print_sys

CONFIG_DIR = os.path.expanduser("~/.hackernotes")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.toml")

config = {}

# if config file exists, load it
if os.path.exists(CONFIG_PATH):
    config = toml.load(CONFIG_PATH)
else:
    # Ensure the CONFIG_DIR exists
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        print_sys(f"[+] Created configuration directory at {CONFIG_DIR}")

    # create default config file
    config = {
        "db_path": os.path.join(CONFIG_DIR, "notes.db"),
        "active_workspace": "DEFAULT",
        "model_backend": "ollama",
        "ollama_config": {
            "model": "llama2",
            "api_key": None,
            "api_url": None,
        },
    }
    with open(CONFIG_PATH, "w") as f:
        toml.dump(config, f)
    print_sys(f"[+] Created config file at {CONFIG_PATH}")

# DB_PATH = config.get("db_path", os.path.join(CONFIG_DIR, "notes.db"))
# ACTIVE_WORKSPACE = config.get("active_workspace", "DEFAULT")
# MODEL_BACKEND = config.get("model_backend", "ollama")

def update_config(**kwargs):
    """
    Update the configuration file with new values.
    """
    global config
    config.update(kwargs)
    with open(CONFIG_PATH, "w") as f:
        toml.dump(config, f)
    print_sys(f"[+] Updated config file at with new values: {kwargs}")