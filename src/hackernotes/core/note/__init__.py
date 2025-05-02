from pydantic import BaseModel
import os

from hackernotes.utils.term import fsys, print_err, print_warn

from .meta import NoteMeta
from ..workspace import Workspace
from ..snippets import Snippets
from ..annotations import Annotations

class Note(BaseModel):
    """Note model."""
    meta: NoteMeta = NoteMeta()
    snippets: Snippets = Snippets()
    annotations: Annotations = Annotations()

    @staticmethod
    def __get_path__(id: str) -> str:
        """Returns the file path of the note given the id and active workspace."""
        # Get the current workspace
        ws = Workspace.get()
        return os.path.join(ws.base_dir, f"{id}.hnote")

    @property
    def file_path(self) -> str:
        """Returns the file path of the note using the metadata id."""
        return self.__get_path__(self.meta.id)
    
    # --- Note Methods ---

    def add(self, content: str):
        """Adds a snippet to the note."""
        self.snippets.add(content)
        self.meta.touch()
        self.update_annotations()

    def update_annotations(self):
        """Updates the annotations of the note: collect all the snippets' annotations."""
        self.annotations = Annotations(
            tags=self.snippets.tags,
            # TODO entities=self.snippets.entities, etc
        )

    def remove(self, confirm: bool = True):
        """Removes the note from the workspace."""
        if confirm:
            # Ask for confirmation
            confirm = input(fsys(f"Are you sure you want to remove the note {self.meta.id}? (y/n) "))
            if confirm.lower() != "y":
                print_err("Note removal cancelled.")
                return
        # Remove the note file
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            print_err(f"Note with id {self.meta.id} not found in the current workspace.")
            return
        print_warn(f"Note {self.meta.id} removed.")

    # --- Serialization Methods ---

    def __get_filler__(self, title: str) -> str:
        """Returns a filler string for the given title."""
        fill_width = 80
        filler = "=" * ((fill_width - 2 - len(title))//2)
        return f"{filler} {title} {filler}\n"[-fill_width:]

    def dumps(self) -> str:
        """Serialize the note to a string."""
        # Make sure to update the annotations before dumping the note
        self.update_annotations()
        # Create the data string
        data = ""
        # Dump metadata 
        data += self.__get_filler__("HACKERNOTE METADATA")
        data += self.meta.dumps()
        # Dump snippets
        data += self.__get_filler__("SNIPPETS")
        data += self.snippets.dumps()
        # Dump annotations
        data += self.__get_filler__("ANNOTATIONS")
        data += self.annotations.dumps()
        # Dump closing line
        data += self.__get_filler__("END OF HACKERNOTE")
        return data

    def parse_hackernote_sections(text):
        import re
        """Parse the sections of a hackernote."""
        sections = {}
        
        # Find all matches for section headers and their positions
        matches = list(re.finditer(r"^=+\s*(.*?)\s*=+$", text, re.MULTILINE))
        
        for i in range(len(matches)):
            title = matches[i].group(1).strip().upper()
            start = matches[i].end()
            end = matches[i+1].start() if i + 1 < len(matches) else len(text)
            content = text[start:end].strip()
            sections[title] = content

        return sections
    
    @classmethod
    def loads(cls, content: str) -> "Note":
        """Deserialize the note from a string."""
        # Parse the sections
        sections = cls.parse_hackernote_sections(content)
        # Deserialize the sections
        meta = NoteMeta.loads(sections["HACKERNOTE METADATA"])
        annotations = Annotations.loads(sections["ANNOTATIONS"])
        snippets = Snippets.loads(sections["SNIPPETS"], ext_annotations=annotations)
        # Create the note object
        note = Note(meta=meta, snippets=snippets, annotations=annotations)
        return note
    
    # --- File Operations ---

    def persist(self):
        """Persists the note to a file."""
        with open(self.file_path, "w") as f:
            f.write(self.dumps())

    @classmethod
    def read(cls, id: str) -> "Note":
        """Reads the note from a file."""
        try:
            with open(cls.__get_path__(id), "r") as f:
                content = f.read()
        except FileNotFoundError:
            print_err(f"Note with id {id} not found in the current workspace.")
            return None
        return cls.loads(content)