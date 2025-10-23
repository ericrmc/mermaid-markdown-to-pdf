#!/bin/bash

# Build script for the containerized markdown to PDF converter

set -e

# Configuration
IMAGE_NAME="markdown-pdf-converter"
TAG="latest"
FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

echo "=== Building Markdown to PDF Converter Container ==="
echo "Image: ${FULL_IMAGE_NAME}"
echo ""

# Build the Docker image
echo "Building Docker image..."
docker build -t "${FULL_IMAGE_NAME}" .

echo ""
echo "✓ Build completed successfully!"
echo ""
echo "Usage examples:"
echo "  # Single file"
echo "  docker run --rm -v \$(pwd):/workspace ${FULL_IMAGE_NAME} README.md"
echo ""
echo "  # Multiple files"
echo "  docker run --rm -v \$(pwd):/workspace ${FULL_IMAGE_NAME} *.md"
echo ""
echo "  # Process folder"
echo "  docker run --rm -v \$(pwd):/workspace ${FULL_IMAGE_NAME} --folder docs/"
echo ""
echo "  # Custom output directory"
echo "  docker run --rm -v \$(pwd):/workspace ${FULL_IMAGE_NAME} --output-dir pdfs/ *.md"
echo ""
echo "  # Check dependencies"
echo "  docker run --rm ${FULL_IMAGE_NAME} --check-deps"
echo ""
echo "To create an alias for easier usage:"
echo "  alias md2pdf='docker run --rm -v \$(pwd):/workspace ${FULL_IMAGE_NAME}'"
echo "  md2pdf README.md"
echo ""
echo "To test with examples:"
echo "  cd examples && ./convert-examples.sh"