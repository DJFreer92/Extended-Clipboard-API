# Extended Clipboard API v0.1.0 🚀

Initial release of Extended Clipboard API - a FastAPI service for managing clipboard entries with encryption and local-first privacy.

## 🌟 What's New

### Core Features
- **FastAPI REST API** for clipboard management with automatic documentation
- **SQLCipher encryption** for secure, local-first data storage
- **Clipboard persistence** with metadata tracking (source app, timestamps)
- **Tagging system** for organizing clipboard entries
- **Favorites functionality** for marking important clips
- **Flexible filtering** by content, tags, source app, and timestamps

### Architecture Highlights
- **Clean separation** of concerns: Endpoints → Services → Queries → Schema
- **SQL files** for maintainable database queries
- **Comprehensive test suite** with 38 tests and 100% pass rate
- **Docker support** for containerized deployment

### Security & Privacy
- **Encrypted SQLite** database using SQLCipher
- **Local-first** approach - your data never leaves your machine
- **No cloud dependencies** - fully self-contained

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install extended-clipboard-api
```

### From Source
```bash
git clone https://github.com/DJFreer92/Extended-Clipboard-API.git
cd Extended-Clipboard-API
pip install -e .
```

## 🏃‍♂️ Quick Start

1. **Install dependencies:**
   ```bash
   npm install  # For SQLCipher support
   pip install -r requirements.txt
   ```

2. **Initialize database:**
   ```bash
   python scripts/create_db.py
   ```

3. **Start the API:**
   ```bash
   python scripts/run_api.py
   ```

4. **Access documentation:**
   - API docs: http://localhost:8000/docs
   - OpenAPI spec: http://localhost:8000/openapi.json

## 🔧 Tech Stack

- **Python 3.13** runtime
- **FastAPI** framework with Uvicorn server
- **SQLite + SQLCipher** for encrypted data persistence
- **Pydantic** for data validation and serialization
- **Node.js** better-sqlite3-multiple-ciphers for database operations
- **pytest** for comprehensive testing

## 📊 Package Information

- **Source Distribution**: `extended_clipboard_api-0.1.0.tar.gz` (36.2 KB)
- **Wheel Distribution**: `extended_clipboard_api-0.1.0-py3-none-any.whl` (25.0 KB)
- **License**: MIT
- **Python Version**: >=3.13

## 🧪 Testing

All 38 tests passing:
```bash
pytest -q
# ......................................                                          [100%]
# 38 passed in 21.13s
```

## 🎯 Use Cases

- **Developers**: Maintain clipboard history across coding sessions
- **Content creators**: Organize and track copied content
- **Privacy-conscious users**: Keep clipboard data local and encrypted
- **Power users**: Tag and categorize clipboard entries for easy retrieval

## 🔗 Related Projects

- **Desktop App**: [Extended Clipboard Desktop App](https://github.com/DJFreer92/Extended-Clipboard-Desktop-App) - UI that uses this API

## 📝 Documentation

- Full API documentation available at `/docs` endpoint
- Project structure and development guide in [README.md](README.md)
- Changelog in [CHANGELOG.md](CHANGELOG.md)

## 🤝 Contributing

Contributions welcome! Please see our development setup in the README and follow the existing code patterns.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
