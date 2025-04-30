from pydantic import BaseModel
import os

from hackernotes.utils.term import print_err

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

    def add(self, content: str):
        """Adds a snippet to the note."""
        self.snippets.add(content)
        self.meta.touch()

    # --- Serialization Methods ---
    def __get_filler__(self, title: str) -> str:
        """Returns a filler string for the given title."""
        fill_width = 80
        filler = "=" * ((fill_width - 2 - len(title))//2)
        return f"{filler} {title} {filler}\n"[-fill_width:]

    def dumps(self) -> str:
        """Serialize the note to a string."""
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
        # # Use regex to split the content into sections
        # import re
        # sections_divider_start = "=" * 10
        # sections_divider_end = "=" * 10
        # sections = re.split(rf"{sections_divider_start} (.*?) {sections_divider_end}", content) # TODO
        # # Remove empty sections
        # sections = [section.strip() for section in sections if section.strip()]
        # # Check if the sections are valid
        # if len(sections) != 5:
        #     raise ValueError("Invalid note format.")
        # # Extract the sections
        # metadata_section = sections[1]
        # snippets_section = sections[3]
        # annotations_section = sections[4]
        # Parse the sections
        sections = cls.parse_hackernote_sections(content)
        # Deserialize the sections
        meta = NoteMeta.loads(sections["HACKERNOTE METADATA"])
        snippets = Snippets.loads(sections["SNIPPETS"])
        annotations = Annotations.loads(sections["ANNOTATIONS"])
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
        return cls.loads(content)