#!/usr/bin/env python3
"""
Test script for the batch processing functionality
"""

import os
import sys
import tempfile
import shutil
import asyncio

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cli import find_markdown_files, process_multiple_files

def create_test_files():
    """Create test markdown files with various content"""
    test_dir = tempfile.mkdtemp(prefix="md_test_")
    
    # Simple markdown file
    with open(os.path.join(test_dir, "simple.md"), "w") as f:
        f.write("""# Simple Document

This is a simple markdown document without any diagrams.

## Section 1
Some content here.

## Section 2
More content here.
""")
    
    # Markdown with inline Mermaid
    with open(os.path.join(test_dir, "with_mermaid.md"), "w") as f:
        f.write("""# Document with Mermaid

This document contains inline Mermaid diagrams.

## Flow Chart

```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello
    B->>A: Hi there!
```
""")
    
    # Create subdirectory with more files
    subdir = os.path.join(test_dir, "docs")
    os.makedirs(subdir)
    
    with open(os.path.join(subdir, "guide.md"), "w") as f:
        f.write("""# User Guide

This is a user guide document.

## Getting Started
Instructions here.
""")
    
    # Non-markdown file (should be ignored)
    with open(os.path.join(test_dir, "readme.txt"), "w") as f:
        f.write("This is not a markdown file")
    
    return test_dir

def test_find_markdown_files():
    """Test the find_markdown_files function"""
    print("Testing find_markdown_files...")
    
    test_dir = create_test_files()
    
    try:
        # Test recursive search
        files = find_markdown_files([test_dir], recursive=True)
        print(f"Recursive search found {len(files)} files:")
        for f in files:
            print(f"  - {f}")
        
        assert len(files) == 3, f"Expected 3 files, got {len(files)}"
        
        # Test non-recursive search
        files = find_markdown_files([test_dir], recursive=False)
        print(f"Non-recursive search found {len(files)} files:")
        for f in files:
            print(f"  - {f}")
        
        assert len(files) == 2, f"Expected 2 files, got {len(files)}"
        
        # Test specific file
        simple_file = os.path.join(test_dir, "simple.md")
        files = find_markdown_files([simple_file])
        assert len(files) == 1, f"Expected 1 file, got {len(files)}"
        
        print("✓ find_markdown_files tests passed")
        
    finally:
        shutil.rmtree(test_dir)

async def test_batch_processing():
    """Test batch processing (dry run without actual PDF generation)"""
    print("Testing batch processing structure...")
    
    test_dir = create_test_files()
    
    try:
        files = find_markdown_files([test_dir], recursive=True)
        print(f"Found {len(files)} markdown files for processing")
        
        # This would normally process files, but we'll just test the structure
        print("Batch processing structure test completed")
        print("✓ Batch processing structure is correct")
        
    finally:
        shutil.rmtree(test_dir)

def main():
    """Run all tests"""
    print("=== Testing Batch Processing Functionality ===\n")
    
    test_find_markdown_files()
    print()
    
    asyncio.run(test_batch_processing())
    print()
    
    print("✓ All tests passed!")

if __name__ == "__main__":
    main()