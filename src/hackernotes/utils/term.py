import sys

import click
from colorama import Fore, Style

def fsys(content: str):
    """ Format string for system output. """
    return f"{Fore.CYAN}{content}{Style.RESET_ALL}"

def fwarn(content: str):
    """ Format string for warning output. """
    return f"{Fore.YELLOW}{content}{Style.RESET_ALL}"

def ferror(content: str):
    """ Format string for error output. """
    return f"{Fore.RED}{content}{Style.RESET_ALL}"

def fentity(content: str):
    """ Format string for entity output. """
    return f"{Fore.MAGENTA}@{content}{Style.RESET_ALL}"

def ftag(content: str, decorator: str = "#"):
    """ Format string for tag output. """
    return f"{Fore.GREEN}{decorator}{content}{Style.RESET_ALL}"

# def fstatus(status: str):
#     if status == QueueStatus.PENDING:
#         return Fore.YELLOW + status + Style.RESET_ALL
#     elif status == QueueStatus.PROCESSING:
#         return Fore.CYAN + status + Style.RESET_ALL
#     elif status == QueueStatus.COMPLETED:
#         return Fore.GREEN + status + Style.RESET_ALL
#     elif status == QueueStatus.FAILED:
#         return Fore.RED + status + Style.RESET_ALL

# def furl(content: str) -> str:
#     """Formats URLs in gray color."""
#     urls = extract_urls(content)
#     for url in urls:
#         content = content.replace(url, f"{Fore.LIGHTBLACK_EX}{url}{Style.RESET_ALL}")
#     return content

def clear_terminal_line():
    print("\n\033[A                             \033[A")

def clear_terminal():
    print("\033c")

def cursor_up():
    sys.stdout.write("\033[F\033[K")

def print_sys(text: str):
    """
    Print system message to the system console.
    """
    click.echo(fsys(text))
    # sys.stdout.flush()

def print_warn(text: str):
    """
    Print warning message to the system console.
    """
    click.echo(fwarn(text))
    # sys.stdout.flush()

def print_err(text: str):
    """
    Print error message to the system console.
    """
    click.echo(ferror(text))
    # sys.stdout.flush()

def input_sys(prompt: str) -> str:
    """
    Get input from the user with a system prompt.
    """
    return click.prompt(fsys(prompt), type=str)

