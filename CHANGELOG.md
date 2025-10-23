# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-23

### Added
- Initial release of containerized Mermaid Markdown to PDF converter
- Docker containerization with all dependencies (pandoc, LaTeX, Chromium)
- Batch processing support for multiple files and folders
- Support for inline Mermaid code blocks
- Support for external `.mmd` file references
- Recursive and non-recursive folder processing
- Custom output directory option
- Configurable PDF generation options (engine, margins, TOC)
- Configurable image dimensions for Mermaid diagrams
- Comprehensive error handling and progress tracking
- Verbose logging and debugging options
- Dependency validation command
- Complete documentation suite
- Example files demonstrating features
- Build automation scripts
- Docker Compose configuration
- CI/CD integration examples

### Features
- **Input Methods**:
  - Single file conversion
  - Multiple file conversion
  - Glob pattern support (`*.md`)
  - Folder processing with `--folder` option
  - Recursive/non-recursive directory traversal

- **Output Options**:
  - Custom output file names
  - Custom output directories
  - Batch output organization

- **PDF Generation**:
  - Multiple LaTeX engine support (XeLaTeX, LuaLaTeX, PDFLaTeX)
  - Automatic engine fallback
  - Configurable page margins
  - Table of contents generation
  - Configurable TOC depth

- **Mermaid Processing**:
  - All Mermaid diagram types supported
  - Inline code block rendering
  - External `.mmd` file references
  - Configurable image dimensions
  - High-quality PNG output

- **Developer Experience**:
  - Zero local installation required
  - Cross-platform compatibility
  - Comprehensive documentation
  - Example files included
  - Easy alias creation
  - CI/CD ready

### Documentation
- README.md - Main documentation
- GETTING-STARTED.md - Step-by-step guide
- DOCKER-USAGE.md - Docker-specific details
- DEPLOYMENT.md - Production deployment guide
- CONTRIBUTING.md - Contribution guidelines
- examples/ - Working examples with documentation

### Container Specifications
- Base: Python 3.11 slim
- Size: ~2GB (includes complete LaTeX distribution)
- Memory: 1-2GB recommended
- All dependencies pre-installed and validated

## [Unreleased]

### Fixed
- **External .mmd file detection** (2024-10-23)
  - Fixed regex pattern to properly detect .mmd file references with optional title attributes
  - Now correctly handles: `![alt](file.mmd "title")` in addition to `![alt](file.mmd)`
  - Resolves issue where second .mmd reference in external-diagrams-example.md was not being converted

### Changed
- **Project Restructuring** (2024-10-23)
  - Reorganized project structure following standard conventions
  - Moved source code to `src/` directory
  - Moved tests to `tests/` directory
  - Moved extended documentation to `docs/` directory
  - Renamed `unified_markdown_pdf_converter.py` → `src/converter.py`
  - Renamed `unified_markdown_pdf_converter_batch.py` → `src/cli.py`
  - Renamed `test-batch.py` → `tests/test_batch.py`
  - Moved `example-usage.sh` → `examples/convert-examples.sh`
  - Updated script to generate PDFs in examples directory
  - Updated all documentation to reflect new structure
  - Updated Dockerfile and entrypoint.sh
  - **Note**: No breaking changes for end users - Docker interface remains identical

### Planned Features
- Web service API wrapper
- Kubernetes deployment configurations
- Performance optimizations for large batches
- Additional output formats (HTML, EPUB)
- Parallel processing for multiple files
- Progress bar for batch operations
- Configuration file support
- Template system for PDF styling
- Custom CSS support for Mermaid diagrams
- Diagram caching for faster rebuilds

### Under Consideration
- GUI wrapper application
- VS Code extension
- GitHub Action for automated documentation
- Pre-built images on Docker Hub
- ARM architecture support
- Reduced container size options
- Plugin system for extensibility

---

## Version History

### Version Numbering

- **Major version** (X.0.0): Breaking changes, major new features
- **Minor version** (0.X.0): New features, backward compatible
- **Patch version** (0.0.X): Bug fixes, minor improvements

### Release Notes Format

Each release includes:
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features to be removed in future versions
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

---

[1.0.0]: https://github.com/yourusername/mermaid-markdown-to-pdf/releases/tag/v1.0.0