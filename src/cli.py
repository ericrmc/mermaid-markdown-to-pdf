#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright
import sys
import os
import glob
import subprocess
import argparse
import re
import tempfile
import uuid
import shutil
import platform
from typing import List, Tuple, Dict, Optional

# Import all functions from the converter module
from converter import (
    validate_dependencies, get_available_pdf_engine, print_dependency_status,
    check_dependencies_or_exit, mermaid_to_image, extract_mermaid_blocks,
    detect_mmd_file_references, resolve_mmd_file_path, read_mmd_files,
    create_temp_mermaid_files, create_temp_mmd_files_for_external,
    render_unified_mermaid_diagrams, render_mermaid_blocks,
    replace_mermaid_with_images, replace_mermaid_and_mmd_with_images,
    create_temp_markdown, generate_pdf_from_markdown, cleanup_temp_files,
    convert_markdown_to_pdf
)

def find_markdown_files(paths: List[str], recursive: bool = True) -> List[str]:
    """Find all markdown files from given paths (files or directories)"""
    markdown_files = []
    
    for path in paths:
        if os.path.isfile(path):
            if path.lower().endswith(('.md', '.markdown')):
                markdown_files.append(path)
            else:
                print(f"⚠ Warning: {path} is not a markdown file, skipping")
        elif os.path.isdir(path):
            if recursive:
                # Recursively find all .md files
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(('.md', '.markdown')):
                            markdown_files.append(os.path.join(root, file))
            else:
                # Only look in the immediate directory
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    if os.path.isfile(file_path) and file.lower().endswith(('.md', '.markdown')):
                        markdown_files.append(file_path)
        else:
            print(f"⚠ Warning: {path} not found, skipping")
    
    return sorted(list(set(markdown_files)))  # Remove duplicates and sort

async def process_multiple_files(input_files: List[str], output_dir: str = None, 
                               pdf_engine: str = None, margin: str = "1in", 
                               include_toc: bool = True, image_width: int = 1200,
                               image_height: int = 800, keep_temp: bool = False,
                               verbose: bool = False) -> Dict[str, str]:
    """Process multiple markdown files and return mapping of input -> output"""
    results = {}
    total_files = len(input_files)
    successful = 0
    failed = 0
    
    print(f"=== Processing {total_files} markdown file(s) ===\n")
    
    for i, input_file in enumerate(input_files, 1):
        print(f"[{i}/{total_files}] Processing: {input_file}")
        
        try:
            # Generate output path
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                base_name = os.path.splitext(os.path.basename(input_file))[0]
                output_pdf = os.path.join(output_dir, f"{base_name}.pdf")
            else:
                # Place PDF next to source file
                base_name = os.path.splitext(input_file)[0]
                output_pdf = f"{base_name}.pdf"
            
            # Convert the file
            result_pdf = await convert_markdown_to_pdf(
                input_markdown=input_file,
                output_pdf=output_pdf,
                pdf_engine=pdf_engine,
                margin=margin,
                include_toc=include_toc,
                image_width=image_width,
                image_height=image_height,
                keep_temp=keep_temp
            )
            
            results[input_file] = result_pdf
            successful += 1
            print(f"✓ [{i}/{total_files}] Success: {input_file} -> {result_pdf}")
            
        except Exception as e:
            print(f"✗ [{i}/{total_files}] Failed: {input_file} - {e}")
            if verbose:
                import traceback
                traceback.print_exc()
            results[input_file] = None
            failed += 1
        
        print()  # Add spacing between files
    
    # Summary
    print(f"=== Batch Processing Complete ===")
    print(f"Total files: {total_files}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if successful > 0:
        print(f"\n✓ Successfully processed files:")
        for input_file, output_file in results.items():
            if output_file:
                print(f"  {input_file} -> {output_file}")
    
    if failed > 0:
        print(f"\n✗ Failed files:")
        for input_file, output_file in results.items():
            if not output_file:
                print(f"  {input_file}")
    
    return results

async def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown with inline Mermaid diagrams to PDF (Batch Processing)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file
  %(prog)s README.md
  
  # Multiple files
  %(prog)s doc1.md doc2.md doc3.md
  
  # All markdown files in directory (recursive)
  %(prog)s --folder docs/
  
  # All markdown files in current directory (non-recursive)
  %(prog)s --folder . --no-recursive
  
  # Custom output directory
  %(prog)s --output-dir ./pdfs/ *.md
  
  # With custom options
  %(prog)s --engine xelatex --margin 0.5in --image-width 1600 README.md

Container Usage:
  # Mount current directory and process files
  docker run -v $(pwd):/workspace your-converter README.md
  
  # Process all markdown files in docs folder
  docker run -v $(pwd):/workspace your-converter --folder docs/
  
  # Custom output directory
  docker run -v $(pwd):/workspace your-converter --output-dir pdfs/ *.md
        """)
    
    # Input options
    input_group = parser.add_argument_group('Input Options')
    input_group.add_argument('inputs', nargs='*', help='Input markdown files or use --folder')
    input_group.add_argument('--folder', '-f', metavar='DIR',
                           help='Process all markdown files in directory')
    input_group.add_argument('--no-recursive', action='store_true',
                           help='Don\'t search subdirectories when using --folder')
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('-o', '--output', help='Output PDF file (single file mode only)')
    output_group.add_argument('--output-dir', '-d', metavar='DIR',
                            help='Output directory for multiple files (default: same as input)')
    
    # PDF Generation Options
    pdf_group = parser.add_argument_group('PDF Generation Options')
    pdf_group.add_argument('--engine', choices=['xelatex', 'lualatex', 'pdflatex'], 
                          default=None,
                          help='PDF engine to use (default: auto-detect best available)')
    pdf_group.add_argument('--margin', default='1in', 
                          metavar='SIZE',
                          help='Page margins (default: 1in). Examples: 0.5in, 2cm, 20mm')
    pdf_group.add_argument('--no-toc', action='store_true', 
                          default=False,
                          help='Disable table of contents generation')
    pdf_group.add_argument('--toc-depth', type=int, default=3, 
                          metavar='N',
                          help='Table of contents depth (default: 3)')
    
    # Image Processing Options
    image_group = parser.add_argument_group('Image Processing Options')
    image_group.add_argument('--image-width', type=int, default=1200, 
                            metavar='PIXELS',
                            help='Mermaid image width in pixels (default: 1200)')
    image_group.add_argument('--image-height', type=int, default=800, 
                            metavar='PIXELS',
                            help='Mermaid image height in pixels (default: 800)')
    
    # Utility Options
    util_group = parser.add_argument_group('Utility Options')
    util_group.add_argument('--check-deps', action='store_true', 
                           default=False,
                           help='Check system dependencies and exit')
    util_group.add_argument('--keep-temp', action='store_true', 
                           default=False,
                           help='Keep temporary files for debugging')
    util_group.add_argument('--verbose', '-v', action='store_true', 
                           default=False,
                           help='Enable verbose output')
    
    # Legacy Options (for backward compatibility)
    legacy_group = parser.add_argument_group('Legacy Options')
    legacy_group.add_argument('--single', nargs=2, metavar=('INPUT', 'OUTPUT'),
                             help='Convert single MMD file: --single input.mmd output.png')
    legacy_group.add_argument('--legacy', action='store_true',
                             default=False,
                             help='Run legacy end-to-end process')
    
    args = parser.parse_args()
    
    # Handle dependency check
    if args.check_deps:
        dependencies = validate_dependencies()
        print_dependency_status(dependencies)
        
        missing_required = []
        for dep_name, dep_info in dependencies.items():
            if dep_info['required'] and dep_info['status'] == 'missing':
                missing_required.append(dep_name)
        
        available_engine = get_available_pdf_engine(dependencies)
        
        if missing_required or not available_engine:
            print("✗ System is not ready for PDF conversion")
            sys.exit(1)
        else:
            print("✓ System is ready for PDF conversion")
            sys.exit(0)
    
    # Handle legacy modes
    if args.single:
        # Single file mode (backward compatibility)
        input_file, output_file = args.single
        
        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} not found")
            sys.exit(1)
        
        with open(input_file, 'r') as f:
            mermaid_code = f.read()
        
        await mermaid_to_image(mermaid_code, output_file, args.image_width, args.image_height)
        print(f"Successfully converted {input_file} to {output_file}")
        sys.exit(0)
        
    elif args.legacy:
        # Legacy end-to-end mode - not implemented in batch version
        print("Legacy mode not available in batch version. Use original script.")
        sys.exit(1)
    
    # Determine input files
    input_files = []
    
    if args.folder:
        # Process folder
        if not os.path.isdir(args.folder):
            print(f"Error: Directory {args.folder} not found")
            sys.exit(1)
        
        input_files = find_markdown_files([args.folder], recursive=not args.no_recursive)
        
        if not input_files:
            print(f"No markdown files found in {args.folder}")
            sys.exit(1)
        
        print(f"Found {len(input_files)} markdown file(s) in {args.folder}")
        if args.verbose:
            for f in input_files:
                print(f"  - {f}")
        print()
        
    elif args.inputs:
        # Process specified files/patterns
        for pattern in args.inputs:
            if '*' in pattern or '?' in pattern:
                # Handle glob patterns
                matches = glob.glob(pattern)
                if matches:
                    input_files.extend(find_markdown_files(matches))
                else:
                    print(f"⚠ Warning: No files match pattern: {pattern}")
            else:
                # Handle individual files/directories
                input_files.extend(find_markdown_files([pattern]))
        
        if not input_files:
            print("No valid markdown files found")
            sys.exit(1)
    
    else:
        # No input specified
        parser.print_help()
        sys.exit(1)
    
    # Remove duplicates and sort
    input_files = sorted(list(set(input_files)))
    
    # Validate single file mode
    if len(input_files) == 1 and args.output and not args.output_dir:
        # Single file with specific output
        try:
            output_pdf = await convert_markdown_to_pdf(
                input_markdown=input_files[0],
                output_pdf=args.output,
                pdf_engine=args.engine,
                margin=args.margin,
                include_toc=not args.no_toc,
                image_width=args.image_width,
                image_height=args.image_height,
                keep_temp=args.keep_temp
            )
            print(f"\n=== Conversion completed successfully! ===")
            print(f"Generated: {output_pdf}")
            sys.exit(0)
        except Exception as e:
            print(f"\n=== Conversion failed ===")
            print(f"Error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    # Batch processing mode
    try:
        results = await process_multiple_files(
            input_files=input_files,
            output_dir=args.output_dir,
            pdf_engine=args.engine,
            margin=args.margin,
            include_toc=not args.no_toc,
            image_width=args.image_width,
            image_height=args.image_height,
            keep_temp=args.keep_temp,
            verbose=args.verbose
        )
        
        # Check if any files were processed successfully
        successful_count = sum(1 for result in results.values() if result is not None)
        
        if successful_count > 0:
            print(f"\n✓ Batch processing completed with {successful_count} successful conversions")
            sys.exit(0)
        else:
            print(f"\n✗ Batch processing failed - no files were converted successfully")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n=== Batch processing failed ===")
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())