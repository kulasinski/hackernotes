from hackernotes.core.note import Note
from hackernotes.core.note.meta import NoteMeta
from hackernotes.core.snippets import Snippets
from hackernotes.core.annotations import Annotations

def create_test_note(id: str = None) -> Note:
    snippets = Snippets()
    snippets.add("This is a test snippet.")
    snippets.add("This is another test snippet.")

    annotations = Annotations()
    annotations.add_tag("test")
    annotations.add_tag("example")

    note = Note(
        meta=NoteMeta(
            id=id,
            title="Test Note",
        ),
        snippets=snippets,
        annotations=annotations,
    )

    return note

def test_note_create():
    """Test the creation of a note."""

    note = create_test_note()

    assert note is not None
    assert note.meta is not None
    assert note.meta.title == "Test Note"
    assert note.meta.id is not None
    assert note.snippets is not None
    assert note.snippets.length == 2
    assert note.annotations is not None
    assert note.annotations.tags is not None
    assert len(note.annotations.tags) == 2
    assert note.annotations.has_tag("test")
    assert note.annotations.has_tag("example")

def test_note_dump_and_load():
    """Test the dump and load of a note."""

    note = create_test_note()

    # Dump the note to a string
    dumped_note = note.dumps()

    assert dumped_note is not None
    assert isinstance(dumped_note, str)
    assert len(dumped_note) > 0

    # Load the note from the string
    loaded_note = Note.loads(dumped_note)
    assert loaded_note is not None
    assert loaded_note.meta is not None
    assert loaded_note.meta.title == "Test Note"
    assert loaded_note.meta.id is not None
    assert loaded_note.snippets is not None
    assert loaded_note.snippets.length == 2
    assert loaded_note.annotations is not None
    assert loaded_note.annotations.tags is not None
    assert len(loaded_note.annotations.tags) == 2
    assert "test" in loaded_note.annotations.tags
    assert "example" in loaded_note.annotations.tags
    assert loaded_note.snippets[0] == "This is a test snippet."
    assert loaded_note.snippets[1] == "This is another test snippet."
    assert loaded_note.meta.id == note.meta.id
    assert loaded_note.meta.created_at == note.meta.created_at
    assert loaded_note.meta.updated_at == note.meta.updated_at
    assert loaded_note.meta.title == note.meta.title
    assert loaded_note.meta.archived == note.meta.archived

def test_note_io():
    """Test the IO operations of a note."""

    note = create_test_note(id="test_id")

    # Persist the note
    note.persist()

    # Read
    loaded_note = Note.read(note.meta.id)

    # Compare
    assert loaded_note is not None
    assert loaded_note.meta is not None
    assert loaded_note.meta.title == "Test Note"
    assert loaded_note.meta.id is not None
    assert loaded_note.snippets is not None
    assert loaded_note.snippets.length == 2
    assert loaded_note.annotations is not None
    assert loaded_note.annotations.tags is not None
    assert len(loaded_note.annotations.tags) == 2
    assert loaded_note.annotations.has_tag("test")
    assert loaded_note.annotations.has_tag("example")
    assert loaded_note.snippets[0] == "This is a test snippet."
    assert loaded_note.snippets[1] == "This is another test snippet."
    assert loaded_note.meta.id == note.meta.id
    assert loaded_note.meta.created_at == note.meta.created_at
    assert loaded_note.meta.updated_at == note.meta.updated_at
    assert loaded_note.meta.title == note.meta.title
    assert loaded_note.meta.archived == note.meta.archived

