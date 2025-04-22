# Contributing to HackerNotes

Thanks for your interest in contributing to **HackerNotes** — a GenAI-supported, terminal-first note-taking tool. Your ideas, feedback, and code help shape this into a powerful tool for everyone.

---

## 🛠️ Local Setup

```bash
# Clone the repo
git clone https://github.com/yourname/hackernotes.git
cd hackernotes

# Install dependencies
poetry install

# Run CLI
poetry run hn --help
```

---

## 📦 Project Structure

```txt
src/hackernotes/       # Main source code
  ├── db/              # Database models and setup
  ├── core/            # Business logic
  ├── cli/             # Command-line interface
  ├── services/        # LLM and sync integrations
  └── utils/           # Small helpers
```

---

## ✅ Contribution Guidelines

1. **Open an Issue** before submitting large PRs.
2. **Small, focused commits** are appreciated.
3. **Write clean, idiomatic Python (3.11+)**.
4. **Use Poetry for dependency management**.
5. **Lint with Ruff / Format with Black**.
6. **Tests are coming** — for now, manual testing is OK.

---

## 🚀 Getting Involved

- 📥 Suggest new CLI commands
- 🧠 Improve prompt engineering logic
- 📚 Write documentation or tutorials
- 🐞 Fix a bug or improve error handling
- 🌍 Translate output or add shell completions

---

## 📄 License
By contributing, you agree your code will be released under the [Apache 2.0 License](LICENSE).

---

Thank you 🙌
— The HackerNotes Maintainer

