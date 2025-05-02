import click
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import HTML

from hackernotes.core.ai import extract_entities_from_text, extract_tags_from_text, extract_time_intelligence_from_text
from hackernotes.core.note import Note
from hackernotes.db import SessionLocal
# from hackernotes.db.query import NoteCRUD
from hackernotes.utils.parsers import entities2line, line2entities, line2tags, tags2line
from hackernotes.utils.term import clear_previous_line, clear_terminal_line, fsys, ftag, print_sys, print_warn

from . import hn

# === AI/LLM Commands ===
@hn.group()
def ai():
    """AI intelligence operations."""
    pass

@ai.command()
def queue():
    """List all queued tasks."""
    pass

@ai.command()
def dequeue():
    """Dequeue a task. Or all tasks if no task is specified."""
    pass

@ai.command()
@click.argument('note_id')
@click.option('--interactive', '-i', is_flag=True, help="Run in interactive mode. Agree to LLM intelligence.")
@click.option('--tags', '-t', is_flag=True, help="Highlight or add tags to the note.")
@click.option('--entities', '-e', is_flag=True, help="Highlight or add entities to the note.")
@click.option('--times', '-ti', is_flag=True, help="Highlight or add time intelligence to the note.")
def run(note_id, interactive, tags, entities, times):
    """Run an AI-magick task on a note."""
    if not note_id:
        print_warn("Note ID is required.")
        return
    
    if not any([tags, entities, times]):
        print_warn("At least one of --tags or --entities must be specified.")
        return
    
    note = Note.read(note_id)
    if not note:
        return
    
    note_body = note.dumps() # note.title + "\n\n" + '\n'.join([snippet.content for snippet in note.snippets])

    if tags:
        print_sys("Extracting tags...")
        tag_set = extract_tags_from_text(note_body)
        clear_previous_line()
    else:
        tag_set = None

        # if entities:
        #     entity_intelligence = extract_entities_from_text(note_body)
        # else:
        #     entity_intelligence = None

        # if times:
        #     time_intelligence = extract_time_intelligence_from_text(note_body)
        # else:
        #     time_intelligence = None
        
    if interactive:
        prompt_session = PromptSession(history=InMemoryHistory())

        # Tags
        if tag_set:
            tags_interactive = prompt_session.prompt(
                    HTML(f"<ansicyan>Tags (edit):</ansicyan> "),
                    default=tags2line(tag_set),
            )
            tag_set = line2tags(tags_interactive)

        # Entities
        # if entity_intelligence:
        #     entities_interactive = prompt_session.prompt(
        #             HTML(f"<ansicyan>Entities (edit):</ansicyan> "),
        #             default=entities2line(entity_intelligence),
        #     )
        #     entity_intelligence = line2entities(entities_interactive)
        #     print(entity_intelligence)
        # Time intelligence
        # TODO 

    else:
        # Tags
        if tag_set:
            print(fsys("Tags:"), ftag(tags2line(tag_set), decorator=""))
        # Entities
        # if entity_intelligence:
        #     print(fsys("Entities:"), ftag(entities2line(entity_intelligence), decorator=""))
        # Time intelligence
        # TODO 

    # Add the tags to the note, wherever they fit. 
    used_tags = set()
    if tags:
        for tag in tag_set:
            for snippet in note.snippets:
                if tag.content in snippet.content and not snippet.annotations.has_tag(tag):
                    snippet.add_tag(tag)
                    used_tags.add(tag)
                    break
    remaining_tags = tag_set - used_tags

    # Create new snippet with the remaining annotations
    ai_snippet_content = tags2line(remaining_tags)
    # TODO add entities and time intelligence to the snippet content

    # Add the remaining (or selected) annotations to the note
    note.add(content=ai_snippet_content)

    # Display the updated note to the user
    print(note.dumps())
    
    # Save to disk
    confirm = input(fsys("Do you want to save the changes? (y/n) "))
    if confirm.lower() != "y":
        print_warn("Changes not saved.")
        return
    note.persist()
    print_sys("Note has been updated.")

    return

@ai.command()
@click.argument('type')
def prompt(type):
    pass

@ai.command()
def chat():
    pass

@ai.command()
@click.argument('note_id')
def generate(note_id):
    pass