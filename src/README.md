# Source Code

This directory contains the core application code for the Markdown to PDF converter.

## Files

### `converter.py`
**Core conversion logic**

Contains all the fundamental functionality for converting Markdown files with Mermaid diagrams to PDF:

- **Dependency validation**: Check for required system tools (pandoc, LaTeX engines)
- **Mermaid rendering**: Convert Mermaid diagrams to PNG images using Playwright/Chromium
- **Markdown processing**: Parse markdown, extract diagrams, handle external `.mmd` files
- **PDF generation**: Use Pandoc and LaTeX to create professional PDFs
- **File management**: Handle temporary files, cleanup, path resolution

**Key Functions:**
- `convert_markdown_to_pdf()` - Main conversion orchestrator
- `mermaid_to_svg()` - Render Mermaid code to SVG (vector format)
- `extract_mermaid_blocks()` - Find inline Mermaid diagrams
- `detect_mmd_file_references()` - Find external `.mmd` file references
- `generate_pdf_from_markdown()` - Create PDF using Pandoc
- `validate_dependencies()` - Check system requirements

### `cli.py`
**Command-line interface and batch processing**

Provides the user-facing CLI and handles batch operations:

- **Argument parsing**: Process command-line options and flags
- **File discovery**: Find markdown files (recursive/non-recursive)
- **Batch processing**: Handle multiple files efficiently
- **Progress tracking**: Show conversion progress and status
- **Error handling**: Graceful error handling for batch operations
- **Help system**: Display usage information and examples

**Key Functions:**
- `main()` - CLI entry point
- `find_markdown_files()` - Discover markdown files in directories
- `process_multiple_files()` - Batch conversion orchestrator

**Imports from converter.py:**
All core conversion functions are imported and used by the CLI.

## Architecture

```
┌─────────────────────────────────────────────┐
│           Docker Container                   │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │         entrypoint.sh                   │ │
│  │  (Container entry point)                │ │
│  └──────────────┬──────────────────────────┘ │
│                 │                             │
│                 ▼                             │
│  ┌────────────────────────────────────────┐ │
│  │           cli.py                        │ │
│  │  • Parse arguments                      │ │
│  │  • Discover files                       │ │
│  │  • Orchestrate batch processing         │ │
│  └──────────────┬──────────────────────────┘ │
│                 │                             │
│                 ▼                             │
│  ┌────────────────────────────────────────┐ │
│  │         converter.py                    │ │
│  │  • Validate dependencies                │ │
│  │  • Render Mermaid diagrams              │ │
│  │  • Process markdown                     │ │
│  │  • Generate PDFs                        │ │
│  └──────────────┬──────────────────────────┘ │
│                 │                             │
│                 ▼                             │
│  ┌────────────────────────────────────────┐ │
│  │      External Dependencies              │ │
│  │  • Playwright (Chromium)                │ │
│  │  • Pandoc                               │ │
│  │  • LaTeX engines                        │ │
│  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Usage

### Direct Python Usage (Development)

```python
# Using the converter directly
from converter import convert_markdown_to_pdf
import asyncio

async def main():
    output = await convert_markdown_to_pdf(
        input_markdown="document.md",
        output_pdf="output.pdf",
        image_width=1200,
        image_height=800
    )
    print(f"Generated: {output}")

asyncio.run(main())
```

```python
# Using the CLI module
from cli import find_markdown_files, process_multiple_files
import asyncio

async def main():
    files = find_markdown_files(["docs/"], recursive=True)
    results = await process_multiple_files(
        input_files=files,
        output_dir="pdfs/"
    )
    print(f"Processed {len(results)} files")

asyncio.run(main())
```

### Container Usage (Production)

The container automatically uses these modules:

```bash
# Single file
docker run --rm -v $(pwd):/workspace markdown-pdf-converter document.md

# Batch processing
docker run --rm -v $(pwd):/workspace markdown-pdf-converter --folder docs/
```

## Dependencies

### Python Packages
- `playwright>=1.40.0` - Browser automation for Mermaid rendering
- Standard library modules (asyncio, subprocess, argparse, etc.)

### System Dependencies
- **pandoc** - Markdown to PDF conversion
- **xelatex/lualatex/pdflatex** - PDF generation engines
- **chromium** - Installed by Playwright for diagram rendering

## Development

### Running Tests

```bash
# From project root
python tests/test_batch.py
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions
- Keep functions focused and single-purpose

### Adding New Features

1. **Core functionality** → Add to `converter.py`
2. **CLI options** → Add to `cli.py`
3. **Tests** → Add to `tests/test_batch.py`
4. **Documentation** → Update relevant docs in `docs/`

## Error Handling

Both modules implement comprehensive error handling:

- **converter.py**: Handles file I/O errors, rendering failures, PDF generation issues
- **cli.py**: Handles batch processing errors, continues on individual file failures

## Performance Considerations

- **Async operations**: Mermaid rendering uses async/await for efficiency
- **Batch processing**: Multiple files processed in sequence (parallel processing planned)
- **Temporary files**: Cleaned up automatically unless `--keep-temp` flag used
- **Memory usage**: ~1-2GB recommended for complex documents

## Future Enhancements

Planned improvements:
- Parallel processing for multiple files
- Diagram caching for faster rebuilds
- Plugin system for extensibility
- Additional output formats (HTML, EPUB)
- Web service API wrapper

## Contributing

See [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for guidelines on contributing to this codebase.

## License

See [LICENSE](../LICENSE) file in project root.
