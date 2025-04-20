# hackernotes/main.py

import sys
import logging

from .cli import hn  # entrypoint CLI group (Click)
# register CLI commands
from .cli import general, note, annotation, aliases, graph, workspace, ai

# Optional: setup logging or tracing
logging.basicConfig(level=logging.INFO)

def main():
    try:
        hn()  # invoke CLI
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(1)
    except Exception as e:
        logging.exception("Unhandled exception:")
        sys.exit(2)

if __name__ == "__main__":
    main()
