# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-08-16

### Added

- Initial release of Extended Clipboard API
- FastAPI-based REST API for clipboard management
- SQLCipher integration for encrypted data storage
- Clipboard entry persistence with metadata tracking
- Tagging system for organizing clipboard entries
- Favorites functionality for important clips
- Source application tracking
- Flexible filtering and search capabilities
- Clean layered architecture (Endpoints → Services → Queries → Schema)
- Comprehensive test suite with pytest
- Docker support for containerized deployment
- Node.js runner for SQLCipher database operations

### Features

- **Core API Endpoints:**
  - Create, read, update, delete clipboard entries
  - Add/remove tags and favorites
  - Filter clips by content, tags, source app, and timestamps
  - Bulk operations for data management

- **Data Security:**
  - Encrypted SQLite database using SQLCipher
  - Local-first approach for privacy

- **Developer Experience:**
  - Well-documented API with FastAPI automatic documentation
  - Clean separation of concerns across application layers
  - SQL queries stored as files for maintainability
  - Comprehensive test coverage

### Technical Details

- Python 3.13 runtime
- FastAPI framework with Uvicorn server
- SQLite + SQLCipher for encrypted data persistence
- Pydantic for data validation and serialization
- pytest for testing framework
- Node.js better-sqlite3-multiple-ciphers for database operations
