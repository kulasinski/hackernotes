
from hackernotes.core.note import Note
from hackernotes.core.note.meta import NoteMeta


def test_automatic_tag_parsing():
    """Test automatic tag parsing."""
    
    note = Note(
        meta=NoteMeta(
            id="test_note_tag_parsing",
            title="Tag Note",
        )
    )

    note.add("This is a test snippet with #tag1 and #tag2.")
    note.add("This is another snippet with #tag3.")
    note.add("This is a snippet with no tags...")

    # Check if the tags are correctly extracted
    assert note.snippets[0].annotations.has_tag("tag1")
    assert note.snippets[0].annotations.has_tag("tag2")
    assert note.snippets[1].annotations.has_tag("tag3")
    assert note.annotations.has_tag("tag1")
    assert note.annotations.has_tag("tag2")
    assert note.annotations.has_tag("tag3")
    assert len(note.annotations.tags) == 3

    note.persist()

    # read the note from the file
    loaded_note = Note.read(note.meta.id)
    assert loaded_note.snippets[0].annotations.has_tag("tag1")
    assert loaded_note.snippets[0].annotations.has_tag("tag2")
    assert loaded_note.snippets[1].annotations.has_tag("tag3")
    assert not loaded_note.snippets[0].annotations.has_tag("tag3")
    assert len(loaded_note.annotations.tags) == 3

    note.remove(confirm=False)
    