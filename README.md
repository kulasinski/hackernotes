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

---

## 🤝 Contributing
Pull requests, suggestions, and questions are welcome! Please open an issue or discussion to get started.

---

## 📄 License
Apache License 2.0. See `LICENSE` file for details.

