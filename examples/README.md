# Examples

This directory contains example markdown files demonstrating various features of the converter.

## Quick Start

**Convert all examples at once:**
```bash
cd examples
./convert-examples.sh
```

This will generate PDFs for all example files in this directory.

## Files

### `simple-example.md`
Demonstrates inline Mermaid diagrams with:
- Flowchart
- Sequence diagram

**Convert:**
```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter examples/simple-example.md
```

### `external-diagrams-example.md`
Demonstrates external `.mmd` file references with:
- Architecture diagram from external file
- Workflow diagram from external file
- Mixed inline and external diagrams

**Convert:**
```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter examples/external-diagrams-example.md
```

### `diagrams/` Directory
Contains reusable Mermaid diagram files:
- `architecture.mmd` - System architecture diagram
- `workflow.mmd` - User workflow diagram

## Batch Processing Examples

### Convert All Examples

```bash
# Convert all example files
docker run --rm -v $(pwd):/workspace markdown-pdf-converter examples/*.md

# Convert with custom output directory
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --output-dir examples/pdfs/ examples/*.md
```

### Process Examples Folder

```bash
# Process entire examples folder
docker run --rm -v $(pwd):/workspace markdown-pdf-converter --folder examples/

# Non-recursive (only top-level files)
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --folder examples/ --no-recursive
```

## Expected Output

After conversion, you should see PDF files generated:
- `simple-example.pdf` - Contains rendered flowchart and sequence diagram
- `external-diagrams-example.pdf` - Contains all diagrams from external files

## Customization Examples

### High-Resolution Diagrams

```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --image-width 2400 --image-height 1600 \
  examples/simple-example.md
```

### Custom Margins and No TOC

```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --margin 0.5in --no-toc \
  examples/simple-example.md
```

### Verbose Output for Debugging

```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --verbose --keep-temp \
  examples/simple-example.md
```

## Creating Your Own Examples

1. Create a new `.md` file in this directory
2. Add Mermaid diagrams (inline or external references)
3. Convert using `./convert-examples.sh` or the commands above
4. Check the generated PDF

For external diagrams:
1. Create `.mmd` files in the `diagrams/` directory
2. Reference them in your markdown: `![Description](./diagrams/your-diagram.mmd)`
3. The converter will automatically find and render them

## Scripts

### `convert-examples.sh`
Automated script to convert all example files to PDF. Run from this directory:
```bash
./convert-examples.sh
```

Features:
- Checks for Docker and container image
- Converts all example markdown files
- Generates PDFs in this directory
- Shows conversion results
- Provides additional usage examples