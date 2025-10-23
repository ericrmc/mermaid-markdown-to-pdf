#!/bin/bash

# Convert all example markdown files to PDF
# This script demonstrates the converter and generates PDFs in the examples folder

set -e

IMAGE_NAME="markdown-pdf-converter:latest"

echo "=== Converting Example Markdown Files to PDF ==="
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if image exists
if ! docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
    echo "❌ Container image not found: $IMAGE_NAME"
    echo "Please run ./build.sh from the project root first"
    echo ""
    echo "  cd .."
    echo "  ./build.sh"
    echo "  cd examples"
    echo "  ./convert-examples.sh"
    exit 1
fi

echo "✅ Container image found: $IMAGE_NAME"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to examples directory
cd "$SCRIPT_DIR"

echo "📁 Working directory: $SCRIPT_DIR"
echo ""

# Check for markdown files
if ! ls *.md 1> /dev/null 2>&1; then
    echo "❌ No markdown files found in examples directory"
    exit 1
fi

echo "📄 Found example files:"
ls -1 *.md | grep -v README.md || true
echo ""

# Convert all example markdown files (excluding README.md)
echo "🔄 Converting examples to PDF..."
echo ""

# Convert simple-example.md
if [ -f "simple-example.md" ]; then
    echo "1️⃣  Converting simple-example.md..."
    docker run --rm -v "$SCRIPT_DIR:/workspace" "$IMAGE_NAME" \
        simple-example.md
    echo ""
fi

# Convert external-diagrams-example.md
if [ -f "external-diagrams-example.md" ]; then
    echo "2️⃣  Converting external-diagrams-example.md..."
    docker run --rm -v "$SCRIPT_DIR:/workspace" "$IMAGE_NAME" \
        external-diagrams-example.md
    echo ""
fi

# Check results
echo "=== Conversion Complete ==="
echo ""

if ls *.pdf 1> /dev/null 2>&1; then
    echo "✅ Generated PDFs:"
    ls -lh *.pdf
    echo ""
    echo "📊 Total PDFs created: $(ls -1 *.pdf | wc -l)"
else
    echo "❌ No PDFs were generated"
    exit 1
fi

echo ""
echo "=== Additional Usage Examples ==="
echo ""
echo "# Convert with high-resolution diagrams:"
echo "docker run --rm -v \$(pwd):/workspace $IMAGE_NAME \\"
echo "  --image-width 2400 --image-height 1600 simple-example.md"
echo ""
echo "# Convert without table of contents:"
echo "docker run --rm -v \$(pwd):/workspace $IMAGE_NAME \\"
echo "  --no-toc simple-example.md"
echo ""
echo "# Convert with custom margins:"
echo "docker run --rm -v \$(pwd):/workspace $IMAGE_NAME \\"
echo "  --margin 0.5in simple-example.md"
echo ""
echo "# Keep temporary files for debugging:"
echo "docker run --rm -v \$(pwd):/workspace $IMAGE_NAME \\"
echo "  --keep-temp --verbose simple-example.md"
echo ""

echo "✅ All examples completed successfully!"
echo ""
echo "💡 Tip: Create an alias for easier use:"
echo "   alias md2pdf='docker run --rm -v \$(pwd):/workspace $IMAGE_NAME'"
echo "   md2pdf simple-example.md"
