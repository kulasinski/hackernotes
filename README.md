# HackerNotes

**GenAI-supported note-taking via Terminal. Local-first. Privacy-respecting. Hackable.**

---

## 🚀 Overview
HackerNotes is a terminal-native, AI-augmented personal knowledge management system. Designed for developers, researchers, and structured thinkers, it blends the simplicity of text-based input with the power of modern LLMs.

- Local-first, SQLite-based architecture
- Snippet-by-snippet note input
- Automatic extraction of annotations: `#tags`, `@entities`, `*time`
- Graph-based semantic organization
- LLM-backed enrichment, classification, and generation
- Fully scriptable CLI with plugin-ready architecture

---

## 🧱 Core Features
- 📓 **Notes and Snippets**: Organize your thoughts piece by piece
- 🧠 **LLM Integration**: Enhance, classify, and generate outputs
- 🗂️ **Graph Navigation**: Traverse ideas semantically
- ✨ **Annotations**: Embedded or inferred from your content
- 🔧 **Offline Capable**: Use Ollama or OpenAI
- 🔁 **Syncable**: Dropbox/iCloud support (WIP)

---

## 🖥️ Installation
```bash
# clone
git clone https://github.com/yourname/hackernotes.git
cd hackernotes

# install dependencies
poetry install

# run CLI
poetry run hn

# or for dev
poetry env activate

# initialize DB
hn db init 

# check
sqlite3 ~/.hackernotes/notes.db ".tables"

# clean up 
hn db remove
```

---

## 🧪 Example Usage
```bash
hn new "Meeting with @Mike re: #strategy"
hn note list
hn note show
hn llm chat
hn graph show
```

---

## 🛠 Roadmap Highlights
- ✅ Modular schema with full annotation support
- ✅ Click-based CLI
- 🔜 Web UI (Supabase-backed)
- 🔜 Scheduled prompts and automation
- 🔜 Multi-agent note interaction
- encrypting local and remote .db files for enhanced security

---

## 🤝 Contributing
Pull requests, suggestions, and questions are welcome! Please open an issue or discussion to get started.

---

## 📄 License
Apache License 2.0. See `LICENSE` file for details.

---

## Module Structure

# HackerNotes Python Module Structure (OOP-centric)

```
hackernotes/
├── __init__.py
│
├── cli/                     # CLI command logic (Click handlers)
│   ├── __init__.py
│   ├── note.py
│   ├── workspace.py
│   ├── graph.py
│   ├── ai.py
│   ├── tag.py
│   ├── entity.py
│   ├── time.py
│   └── general.py           # init, clean, aliases
│
├── core/                    # Domain objects & business logic
│   ├── __init__.py
│   ├── note.py              # Note, Snippet classes and logic
│   ├── workspace.py         # Workspace class and settings logic
│   ├── graph.py             # GraphNode and traversal/mutation
│   ├── llm.py               # LLM interaction logic and queue
│   ├── prompt.py            # Prompt and generation logic
│   ├── annotation.py        # Tag, Entity, TimeExpr classes
│   └── automation.py        # TaskQueue and scheduler
│
├── db/                      # Persistence layer
│   ├── __init__.py
│   ├── schema.py            # Table definitions (SQLite/Postgres)
│   ├── models.py            # ORM-style access (custom or SQLModel/Peewee)
│   ├── query.py             # High-level queries and joins
│   └── migrations.py        # Setup, schema upgrades
│
├── services/                # External I/O integrations
│   ├── __init__.py
│   ├── ollama.py            # Ollama wrapper
│   ├── openai.py            # OpenAI API wrapper
│   ├── sync.py              # Cloud sync via Dropbox/iCloud
│   └── export.py            # Markdown/file generation
│
├── utils/                   # Helpers
│   ├── __init__.py
│   ├── uuid.py
│   ├── time.py
│   ├── highlight.py         # for colorizing output
│   └── config.py
│
└── main.py                  # CLI entry point (loads Click commands)
```

The /core module should encapsulate your domain logic — the operations and rules that govern how HackerNotes behaves, beyond persistence or UI.

Think of it as the “brain” layer that coordinates between the database, LLMs, and CLI.

✅ Recommended /core Structure
core/
├── __init__.py
├── note.py              # Note lifecycle logic (e.g. add snippet, auto-annotate)
├── workspace.py         # Session + context switching
├── graph.py             # Walk/expand/assign graph nodes
├── llm.py               # Wrap LLM requests + prompt injection
├── prompt.py            # Prompt types, templates, generator logic
├── annotation.py        # Extraction + merge of #tag, @entity, *time
├── automation.py        # Task queue & scheduler execution logic
✅ What Goes in Each Module?
note.py

NoteService.create_note(...)
NoteService.insert_snippet(...)
Attach annotations to snippets
Reorder snippets
workspace.py

Get/set active workspace
Load workspace settings (LLM config, etc.)
graph.py

Traverse parent/child nodes
Auto-place note under graph node (using LLM or rules)
Extend graph from note content
llm.py

Unified interface to openai, ollama, etc.
Generate, classify, summarize
prompt.py

PromptTemplate class
Render prompt from note
Save responses to DB or file
annotation.py

Regex + LLM-based extractors for:
#tags, @entities, *time
De-duplication, fallback logic
automation.py

Create and enqueue tasks
Run queued tasks on schedule
Result processing
🧠 Summary

Layer	Role
db/	Data persistence and schema
core/	Domain logic, LLMs, graph, rules
cli/	Command parsing and interaction


---

## Full Command List

# HackerNotes CLI Design (alias: `hn`)

# General Structure:
# hn <object> <action> [options]

# Aliases:
# hn show     -> hn note show
# hn new      -> hn note new
# hn list     -> hn note list

# =========================
# General Commands
# =========================
hn init                         # Initialize HackerNotes for first-time use
hn clean                        # Cleanup or reset local state

# =========================
# Note Commands
# =========================
hn note new [<title>]           # Start new note (optional title), enters snippet loop
hn note list [--all]            # List recent (or all) notes
hn note show [<note-id>]       # Show a note (last edited if no ID)
hn note edit [<note-id>]       # Edit a note (last edited if no ID)
hn note archive <note-id>      # Soft delete (mark as archived)
hn note delete <note-id>       # Hard delete
hn note export <note-id>       # Trigger generate to file

# =========================
# Workspace Commands
# =========================
hn workspace new <name>         # Create a new workspace
hn workspace switch <id>        # Set active workspace
hn workspace config             # View or modify workspace config
hn workspace delete <id>        # Permanently remove workspace

# =========================
# Graph Commands
# =========================
hn graph show                   # Display current graph schema
hn graph extend                 # Ask LLM to grow the graph
hn graph place <note-id>        # Manually assign note to graph node(s)

# =========================
# LLM Commands
# =========================
hn llm queue                    # View task queue (pending/completed)
hn llm run                      # Run queued tasks (only if using local model)
hn llm prompt <type>            # Manual prompt (chat, generate, annotate, classify)
hn llm chat                     # Chat with knowledge base (RAG)
hn llm generate <note-id>       # Generate secondary file from a note

# =========================
# Annotation Commands
# =========================
hn tag list [--used]            # List all tags
hn entity list [--used]         # List all entities
hn time list [--used]           # List all temporal expressions
