#!/bin/bash

# Entrypoint script for containerized markdown to PDF converter
# Handles file path resolution and provides helpful usage information

set -e

# Function to show usage
show_usage() {
    echo "Unified Markdown to PDF Converter (Containerized)"
    echo ""
    echo "Usage:"
    echo "  docker run -v \$(pwd):/workspace your-converter [OPTIONS] INPUT [INPUT...]"
    echo ""
    echo "Examples:"
    echo "  # Convert single file"
    echo "  docker run -v \$(pwd):/workspace your-converter README.md"
    echo ""
    echo "  # Convert multiple files"
    echo "  docker run -v \$(pwd):/workspace your-converter doc1.md doc2.md"
    echo ""
    echo "  # Convert all markdown files in current directory"
    echo "  docker run -v \$(pwd):/workspace your-converter *.md"
    echo ""
    echo "  # Convert with custom options"
    echo "  docker run -v \$(pwd):/workspace your-converter --engine xelatex --margin 0.5in README.md"
    echo ""
    echo "  # Process folder (finds all .md files recursively)"
    echo "  docker run -v \$(pwd):/workspace your-converter --folder docs/"
    echo ""
    echo "Note: Files are processed in /workspace which should be mounted to your local directory"
}

# If no arguments provided, show usage
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

# If help requested, show usage
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_usage
    exit 0
fi

# Execute the CLI script with all arguments
exec python /app/cli.py "$@"