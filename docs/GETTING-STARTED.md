# Getting Started Guide

This guide will walk you through setting up and using the Mermaid Markdown to PDF Converter.

## Prerequisites

The only requirement is Docker:

- **Docker Desktop** (for macOS/Windows): [Download here](https://www.docker.com/products/docker-desktop)
- **Docker Engine** (for Linux): [Installation guide](https://docs.docker.com/engine/install/)

Verify Docker is installed:
```bash
docker --version
```

## Installation

### Step 1: Get the Code

```bash
# Clone the repository
git clone <your-repo-url>
cd mermaid-markdown-to-pdf
```

### Step 2: Build the Container

```bash
# Make the build script executable
chmod +x build.sh

# Build the Docker image (this may take 5-10 minutes)
./build.sh
```

The build process will:
- Download Python 3.11 base image
- Install system dependencies (pandoc, LaTeX engines)
- Install Python packages
- Set up Playwright with Chromium
- Configure the container environment

### Step 3: Verify Installation

```bash
# Check that dependencies are properly installed
docker run --rm markdown-pdf-converter --check-deps
```

You should see output confirming all dependencies are available.

## Your First Conversion

### Example 1: Convert a Simple File

Create a test markdown file:

```bash
cat > test.md << 'EOF'
# My First Document

## Simple Flowchart

```mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
```

## Content

This is a test document with a Mermaid diagram.
EOF
```

Convert it to PDF:

```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter test.md
```

You should now have `test.pdf` in your current directory!

### Example 2: Try the Included Examples

```bash
# Convert the simple example
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  examples/simple-example.md

# Convert the external diagrams example
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  examples/external-diagrams-example.md

# Convert all examples at once
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  examples/*.md
```

## Common Usage Patterns

### Pattern 1: Single Document Conversion

```bash
# Basic conversion
docker run --rm -v $(pwd):/workspace markdown-pdf-converter document.md

# With custom output name
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  -o my-output.pdf document.md
```

### Pattern 2: Batch Processing

```bash
# All markdown files in current directory
docker run --rm -v $(pwd):/workspace markdown-pdf-converter *.md

# All files in a specific folder
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --folder docs/

# Multiple specific files
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  intro.md guide.md reference.md
```

### Pattern 3: Custom Output Directory

```bash
# Create PDFs in a separate directory
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --output-dir pdfs/ *.md
```

### Pattern 4: High-Quality Diagrams

```bash
# Increase diagram resolution
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --image-width 2400 --image-height 1600 document.md
```

## Creating an Alias (Recommended)

To avoid typing the long Docker command every time, create an alias:

### For Bash/Zsh (Linux/macOS)

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias md2pdf='docker run --rm -v $(pwd):/workspace markdown-pdf-converter'
```

Reload your shell:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

### For Windows PowerShell

Add to your PowerShell profile:

```powershell
function md2pdf { docker run --rm -v ${PWD}:/workspace markdown-pdf-converter $args }
```

### Using the Alias

Now you can simply use:

```bash
md2pdf document.md
md2pdf --folder docs/
md2pdf *.md
```

## Understanding the Command

Let's break down the Docker command:

```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter document.md
```

- `docker run`: Run a Docker container
- `--rm`: Remove container after it finishes (cleanup)
- `-v $(pwd):/workspace`: Mount current directory to `/workspace` in container
- `markdown-pdf-converter`: The image name
- `document.md`: Arguments passed to the converter

## Working with External Diagrams

### Creating External Diagram Files

1. Create a `.mmd` file with your Mermaid code:

```bash
cat > diagram.mmd << 'EOF'
graph TD
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[Action 1]
    C -->|No| E[Action 2]
    D --> F[End]
    E --> F
EOF
```

2. Reference it in your markdown:

```markdown
# My Document

## Architecture

![System Architecture](./diagram.mmd)
```

3. Convert:

```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter document.md
```

The converter will automatically find and render the external diagram.

## Organizing Your Project

Recommended project structure:

```
my-project/
├── README.md                 # Main documentation
├── docs/
│   ├── guide.md
│   ├── api.md
│   └── reference.md
├── diagrams/
│   ├── architecture.mmd
│   ├── workflow.mmd
│   └── database.mmd
└── pdfs/                     # Output directory
```

Convert all documentation:

```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --output-dir pdfs/ README.md docs/*.md
```

## Customization Options

### PDF Appearance

```bash
# Custom margins
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --margin 0.5in document.md

# Disable table of contents
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --no-toc document.md

# Use specific PDF engine
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --engine xelatex document.md
```

### Diagram Quality

```bash
# Standard quality (default)
--image-width 1200 --image-height 800

# High quality
--image-width 2400 --image-height 1600

# Lower quality (faster, smaller files)
--image-width 800 --image-height 600
```

## Troubleshooting

### Issue: "Permission denied" errors

**Solution:** Add user flag (Linux only):
```bash
docker run --rm -v $(pwd):/workspace --user $(id -u):$(id -g) \
  markdown-pdf-converter document.md
```

### Issue: "No markdown files found"

**Solution:** Check that:
- Files have `.md` or `.markdown` extension
- You're in the correct directory
- Files exist: `ls *.md`

### Issue: External diagram not found

**Solution:** 
- Verify the `.mmd` file exists: `ls diagrams/`
- Check the path in your markdown is relative to the markdown file
- Use `--verbose` to see path resolution: `md2pdf --verbose document.md`

### Issue: Container build fails

**Solution:**
- Ensure Docker is running: `docker ps`
- Check internet connection (needed for downloads)
- Try rebuilding: `./build.sh`

### Issue: Slow conversion

**Solution:**
- Reduce image dimensions: `--image-width 800 --image-height 600`
- Process fewer files at once
- Increase Docker memory: Docker Desktop → Settings → Resources

## Getting Help

### View All Options

```bash
docker run --rm markdown-pdf-converter --help
```

### Verbose Output

```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --verbose document.md
```

### Keep Temporary Files

```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --keep-temp document.md
```

This preserves intermediate files for debugging.

### Interactive Shell

```bash
docker run --rm -it -v $(pwd):/workspace \
  --entrypoint /bin/bash markdown-pdf-converter
```

Explore the container environment interactively.

## Next Steps

1. **Try the examples**: Convert the files in the `examples/` directory
2. **Convert your own documents**: Start with simple files and progress to complex ones
3. **Set up an alias**: Make the command easier to use
4. **Integrate with CI/CD**: Automate documentation generation (see DEPLOYMENT.md)
5. **Customize output**: Experiment with different options for your needs

## Additional Resources

- **README.md**: Complete feature list and usage examples
- **docs/DOCKER-USAGE.md**: Detailed Docker-specific information
- **docs/DEPLOYMENT.md**: Production deployment strategies
- **docs/CONTRIBUTING.md**: How to contribute
- **examples/**: Sample files to learn from

## Quick Reference Card

```bash
# Build
./build.sh

# Single file
md2pdf document.md

# Multiple files
md2pdf *.md

# Folder
md2pdf --folder docs/

# Custom output
md2pdf -o output.pdf document.md
md2pdf --output-dir pdfs/ *.md

# High quality
md2pdf --image-width 2400 --image-height 1600 document.md

# Help
md2pdf --help

# Check setup
docker run --rm markdown-pdf-converter --check-deps
```

Happy converting! 🎉