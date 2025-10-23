# Containerized Markdown to PDF Converter

A Docker-containerized version of the unified markdown to PDF converter that handles Mermaid diagrams. This container includes all system dependencies (pandoc, LaTeX engines, Chromium) pre-installed, making it easy to use anywhere without local setup.

## Features

- **Zero Installation**: All dependencies bundled in container
- **Batch Processing**: Handle multiple files and folders
- **Cross-Platform**: Works on any system with Docker
- **File Structure Preservation**: Maintains relative paths for .mmd references
- **Multiple Input Methods**: Single files, multiple files, folders, glob patterns

## Quick Start

### 1. Build the Container

```bash
# Build the image
./build.sh

# Or manually
docker build -t markdown-pdf-converter .
```

### 2. Basic Usage

```bash
# Convert single file
docker run --rm -v $(pwd):/workspace markdown-pdf-converter README.md

# Convert multiple files
docker run --rm -v $(pwd):/workspace markdown-pdf-converter doc1.md doc2.md doc3.md

# Convert all markdown files in current directory
docker run --rm -v $(pwd):/workspace markdown-pdf-converter *.md

# Process entire folder (recursive)
docker run --rm -v $(pwd):/workspace markdown-pdf-converter --folder docs/
```

## Usage Examples

### Single File Processing

```bash
# Basic conversion
docker run --rm -v $(pwd):/workspace markdown-pdf-converter README.md

# With custom output name
docker run --rm -v $(pwd):/workspace markdown-pdf-converter -o my-doc.pdf README.md

# With custom options
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --engine xelatex \
  --margin 0.5in \
  --image-width 1600 \
  README.md
```

### Batch Processing

```bash
# Multiple specific files
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  intro.md guide.md reference.md

# All markdown files (glob pattern)
docker run --rm -v $(pwd):/workspace markdown-pdf-converter *.md

# Process folder recursively
docker run --rm -v $(pwd):/workspace markdown-pdf-converter --folder docs/

# Process folder non-recursively
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --folder docs/ --no-recursive

# Custom output directory
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --output-dir pdfs/ *.md
```

### Advanced Options

```bash
# High-resolution diagrams
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --image-width 2400 --image-height 1600 *.md

# No table of contents
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --no-toc *.md

# Keep temporary files for debugging
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --keep-temp --verbose README.md

# Check container dependencies
docker run --rm markdown-pdf-converter --check-deps
```

## Docker Compose Usage

For easier management, use the included `docker-compose.yml`:

```bash
# Build
docker-compose build

# Run conversions
docker-compose run --rm markdown-converter README.md
docker-compose run --rm markdown-converter --folder docs/
docker-compose run --rm markdown-converter *.md

# Interactive shell for debugging
docker-compose run --rm --entrypoint /bin/bash markdown-converter
```

## Creating an Alias

For frequent use, create a shell alias:

```bash
# Add to your ~/.bashrc or ~/.zshrc
alias md2pdf='docker run --rm -v $(pwd):/workspace markdown-pdf-converter'

# Then use it simply:
md2pdf README.md
md2pdf --folder docs/
md2pdf *.md
```

## File Structure Handling

The container preserves your file structure and handles complex projects:

```
project/
├── README.md                    # Main documentation
├── docs/
│   ├── guide.md                # References ../diagrams/
│   └── api.md                  # References ./schemas/
├── diagrams/
│   ├── architecture.mmd        # External diagram
│   └── flow.mmd               # External diagram
└── schemas/
    └── database.mmd           # External diagram
```

```bash
# Process all files, maintaining references
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --output-dir pdfs/ README.md docs/*.md
```

## Command Line Options

### Input Options
- `inputs`: Input markdown files (can use glob patterns)
- `--folder DIR`: Process all markdown files in directory
- `--no-recursive`: Don't search subdirectories

### Output Options
- `-o, --output FILE`: Output PDF file (single file mode)
- `--output-dir DIR`: Output directory for multiple files

### PDF Generation
- `--engine {xelatex,lualatex,pdflatex}`: PDF engine
- `--margin SIZE`: Page margins (default: 1in)
- `--no-toc`: Disable table of contents
- `--toc-depth N`: TOC depth (default: 3)

### Image Processing
- `--image-width PIXELS`: Mermaid image width (default: 1200)
- `--image-height PIXELS`: Mermaid image height (default: 800)

### Utility Options
- `--check-deps`: Check system dependencies
- `--keep-temp`: Keep temporary files for debugging
- `--verbose`: Enable verbose output

## Troubleshooting

### Permission Issues

If you encounter permission issues:

```bash
# Ensure proper ownership (Linux/macOS)
docker run --rm -v $(pwd):/workspace --user $(id -u):$(id -g) \
  markdown-pdf-converter README.md
```

### Large Files

For projects with many large diagrams:

```bash
# Increase Docker memory limit if needed
docker run --rm -m 2g -v $(pwd):/workspace markdown-pdf-converter \
  --image-width 800 --image-height 600 *.md
```

### Debugging

```bash
# Interactive shell for debugging
docker run --rm -it -v $(pwd):/workspace \
  --entrypoint /bin/bash markdown-pdf-converter

# Check what files are being processed
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --verbose --keep-temp README.md
```

## Container Details

### Included Dependencies
- **Python 3.11** with required packages
- **Pandoc** for markdown to PDF conversion
- **XeLaTeX, LuaLaTeX, PDFLaTeX** for PDF generation
- **Chromium** (via Playwright) for Mermaid rendering
- **Complete LaTeX distribution** for professional PDF output

### Image Size
The container is optimized for functionality over size (~2GB) to include all necessary LaTeX packages for professional PDF output.

### Security
- Runs as non-root user in container
- Only accesses mounted workspace directory
- No network access required after build (except for initial Playwright setup)

## Integration Examples

### CI/CD Pipeline

```yaml
# GitHub Actions example
- name: Generate Documentation PDFs
  run: |
    docker run --rm -v ${{ github.workspace }}:/workspace \
      markdown-pdf-converter --output-dir dist/pdfs/ docs/*.md
```

### Makefile Integration

```makefile
# Makefile
.PHONY: docs
docs:
	docker run --rm -v $(PWD):/workspace \
		markdown-pdf-converter --output-dir dist/ *.md

.PHONY: docs-clean
docs-clean:
	rm -rf dist/*.pdf
```

### Batch Script (Windows)

```batch
@echo off
docker run --rm -v %cd%:/workspace markdown-pdf-converter %*
```

## Performance Tips

1. **Use appropriate image dimensions** - Larger images take more time to render
2. **Process multiple files in one command** - More efficient than multiple container starts
3. **Use --no-toc for simple documents** - Faster processing
4. **Mount only necessary directories** - Faster container startup

## Support

For issues specific to the containerized version:
1. Check Docker logs: `docker logs <container_id>`
2. Use `--verbose` flag for detailed output
3. Use `--check-deps` to verify container setup
4. Try interactive mode for debugging: `docker run -it --entrypoint /bin/bash`