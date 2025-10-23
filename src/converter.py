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

def validate_dependencies() -> Dict[str, Dict[str, str]]:
    """Check for required system dependencies and return status with installation instructions"""
    dependencies = {
        'pandoc': {
            'status': 'missing',
            'required': True,
            'install_instructions': {
                'linux': 'sudo apt-get install pandoc (Ubuntu/Debian) or sudo yum install pandoc (RHEL/CentOS)',
                'darwin': 'brew install pandoc or download from https://pandoc.org/installing.html',
                'windows': 'Download installer from https://pandoc.org/installing.html'
            }
        },
        'xelatex': {
            'status': 'missing',
            'required': False,  # We can fallback to other engines
            'install_instructions': {
                'linux': 'sudo apt-get install texlive-xetex (Ubuntu/Debian) or sudo yum install texlive-xetex (RHEL/CentOS)',
                'darwin': 'brew install --cask mactex or brew install texlive',
                'windows': 'Download MiKTeX from https://miktex.org/ or TeX Live from https://tug.org/texlive/'
            }
        },
        'pdflatex': {
            'status': 'missing',
            'required': False,  # Fallback option
            'install_instructions': {
                'linux': 'sudo apt-get install texlive-latex-base (Ubuntu/Debian) or sudo yum install texlive-latex (RHEL/CentOS)',
                'darwin': 'brew install --cask mactex or brew install texlive',
                'windows': 'Download MiKTeX from https://miktex.org/ or TeX Live from https://tug.org/texlive/'
            }
        },
        'lualatex': {
            'status': 'missing',
            'required': False,  # Fallback option
            'install_instructions': {
                'linux': 'sudo apt-get install texlive-luatex (Ubuntu/Debian) or sudo yum install texlive-luatex (RHEL/CentOS)',
                'darwin': 'brew install --cask mactex or brew install texlive',
                'windows': 'Download MiKTeX from https://miktex.org/ or TeX Live from https://tug.org/texlive/'
            }
        }
    }
    
    # Check pandoc
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, check=True, text=True)
        dependencies['pandoc']['status'] = 'available'
        dependencies['pandoc']['version'] = result.stdout.split('\n')[0]
    except (subprocess.CalledProcessError, FileNotFoundError):
        dependencies['pandoc']['status'] = 'missing'
    
    # Check LaTeX engines
    for engine in ['xelatex', 'pdflatex', 'lualatex']:
        try:
            result = subprocess.run([engine, '--version'], capture_output=True, check=True, text=True)
            dependencies[engine]['status'] = 'available'
            dependencies[engine]['version'] = result.stdout.split('\n')[0]
        except (subprocess.CalledProcessError, FileNotFoundError):
            dependencies[engine]['status'] = 'missing'
    
    return dependencies

def get_available_pdf_engine(dependencies: Dict[str, Dict[str, str]]) -> Optional[str]:
    """Get the best available PDF engine in order of preference"""
    engine_preference = ['xelatex', 'lualatex', 'pdflatex']
    
    for engine in engine_preference:
        if dependencies.get(engine, {}).get('status') == 'available':
            return engine
    
    return None

def print_dependency_status(dependencies: Dict[str, Dict[str, str]]) -> None:
    """Print detailed dependency status and installation instructions"""
    system = platform.system().lower()
    
    print("=== Dependency Check ===")
    
    # Check required dependencies
    missing_required = []
    for dep_name, dep_info in dependencies.items():
        if dep_info['required'] and dep_info['status'] == 'missing':
            missing_required.append(dep_name)
    
    if missing_required:
        print("✗ Missing required dependencies:")
        for dep_name in missing_required:
            dep_info = dependencies[dep_name]
            print(f"  - {dep_name}: {dep_info['install_instructions'].get(system, dep_info['install_instructions']['linux'])}")
        print()
    
    # Check available dependencies
    available_deps = []
    for dep_name, dep_info in dependencies.items():
        if dep_info['status'] == 'available':
            available_deps.append((dep_name, dep_info.get('version', 'unknown version')))
    
    if available_deps:
        print("✓ Available dependencies:")
        for dep_name, version in available_deps:
            print(f"  - {dep_name}: {version}")
        print()
    
    # Check PDF engines specifically
    available_engines = []
    missing_engines = []
    for engine in ['xelatex', 'lualatex', 'pdflatex']:
        if dependencies.get(engine, {}).get('status') == 'available':
            available_engines.append(engine)
        else:
            missing_engines.append(engine)
    
    if available_engines:
        print(f"✓ Available PDF engines: {', '.join(available_engines)}")
        print(f"  Will use: {available_engines[0]} (preferred)")
    else:
        print("✗ No PDF engines available")
        print("  Install at least one of: xelatex, lualatex, or pdflatex")
        print("  Recommended: xelatex (best Unicode and image support)")
    
    if missing_engines:
        print(f"ℹ Missing PDF engines: {', '.join(missing_engines)}")
    
    print()

def check_dependencies_or_exit() -> Dict[str, Dict[str, str]]:
    """Check dependencies and exit if required ones are missing"""
    dependencies = validate_dependencies()
    print_dependency_status(dependencies)
    
    # Check if required dependencies are missing
    missing_required = []
    for dep_name, dep_info in dependencies.items():
        if dep_info['required'] and dep_info['status'] == 'missing':
            missing_required.append(dep_name)
    
    if missing_required:
        print(f"✗ Cannot proceed: Missing required dependencies: {', '.join(missing_required)}")
        print("Please install the missing dependencies and try again.")
        sys.exit(1)
    
    # Check if at least one PDF engine is available
    available_engine = get_available_pdf_engine(dependencies)
    if not available_engine:
        print("✗ Cannot proceed: No PDF engines available")
        print("Please install at least one PDF engine (xelatex recommended) and try again.")
        sys.exit(1)
    
    return dependencies

async def mermaid_to_image(mermaid_code, output_path, width=1200, height=800):
    """Convert Mermaid code to PNG image"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': width, 'height': height})
        
        # Create HTML with Mermaid
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        </head>
        <body>
            <div class="mermaid">
                {mermaid_code}
            </div>
            <script>
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: 'default',
                    flowchart: {{
                        useMaxWidth: false,
                        htmlLabels: true
                    }}
                }});
            </script>
        </body>
        </html>
        """
        
        await page.set_content(html_content)
        await page.wait_for_selector('.mermaid svg', timeout=10000)
        
        # Get the SVG element and take screenshot
        svg_element = await page.query_selector('.mermaid svg')
        await svg_element.screenshot(path=output_path)
        
        await browser.close()

def extract_mermaid_blocks(markdown_content: str) -> List[Tuple[str, str]]:
    """Extract Mermaid code blocks and return (block_content, unique_id) pairs"""
    # Pattern to match ```mermaid code blocks
    pattern = r'```mermaid\n(.*?)\n```'
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    
    # Create unique IDs for each block with enhanced uniqueness
    mermaid_blocks = []
    session_id = uuid.uuid4().hex[:8]  # Single session ID for all inline blocks
    for i, block_content in enumerate(matches):
        unique_id = f"inline_mermaid_{session_id}_{i:03d}"
        mermaid_blocks.append((block_content.strip(), unique_id))
    
    return mermaid_blocks

def detect_mmd_file_references(markdown_content: str) -> List[Tuple[str, str, str]]:
    """Detect .mmd file references and return (file_path, alt_text, unique_id) tuples"""
    # Pattern for .mmd file references in markdown image syntax
    # Matches: ![alt text](path/to/file.mmd) or ![](file.mmd) or ![alt](file.mmd "title")
    # The pattern captures the file path but excludes any optional title in quotes
    pattern = r'!\[([^\]]*)\]\(([^\s)]+\.mmd)(?:\s+"[^"]*")?\)'
    matches = re.findall(pattern, markdown_content)
    
    # Create unique IDs for each reference with enhanced uniqueness
    mmd_references = []
    session_id = uuid.uuid4().hex[:8]  # Single session ID for all external references
    for i, (alt_text, file_path) in enumerate(matches):
        unique_id = f"external_mmd_{session_id}_{i:03d}"
        mmd_references.append((file_path.strip(), alt_text.strip(), unique_id))
    
    return mmd_references

def resolve_mmd_file_path(file_path: str, base_path: str) -> str:
    """
    Resolve relative .mmd file paths relative to the markdown file location
    Handle both absolute and relative paths correctly
    """
    if os.path.isabs(file_path):
        # Absolute path - use as is
        return file_path
    else:
        # Relative path - resolve relative to the base path (directory of markdown file)
        return os.path.join(base_path, file_path)

def read_mmd_files(mmd_references: List[Tuple[str, str, str]], base_path: str) -> Dict[str, Tuple[str, str]]:
    """Read external .mmd files and return mapping of id -> (content, alt_text)"""
    mmd_contents = {}
    
    for file_path, alt_text, unique_id in mmd_references:
        try:
            # Resolve the file path
            resolved_path = resolve_mmd_file_path(file_path, base_path)
            
            # Read the .mmd file content
            with open(resolved_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            mmd_contents[unique_id] = (content, alt_text)
            print(f"✓ Successfully read external .mmd file: {file_path}")
            
        except FileNotFoundError:
            print(f"⚠ Warning: .mmd file not found: {file_path}")
            print(f"  Resolved path: {resolve_mmd_file_path(file_path, base_path)}")
            print("  Skipping this diagram and continuing with others...")
        except PermissionError:
            print(f"⚠ Warning: Permission denied reading .mmd file: {file_path}")
            print("  Check file permissions and try again...")
        except Exception as e:
            print(f"⚠ Warning: Error reading .mmd file {file_path}: {e}")
            print("  Skipping this diagram and continuing with others...")
    
    return mmd_contents

def create_temp_mermaid_files(mermaid_blocks: List[Tuple[str, str]]) -> Dict[str, str]:
    """Create temporary .mmd files for inline blocks and return mapping of id -> filename"""
    temp_files = {}
    
    for block_content, unique_id in mermaid_blocks:
        temp_filename = f"{unique_id}.mmd"
        
        with open(temp_filename, 'w') as f:
            f.write(block_content)
        
        temp_files[unique_id] = temp_filename
    
    return temp_files

def create_temp_mmd_files_for_external(mmd_contents: Dict[str, Tuple[str, str]]) -> Dict[str, str]:
    """Create temporary .mmd files for external references and return mapping of id -> filename"""
    temp_files = {}
    
    for unique_id, (content, alt_text) in mmd_contents.items():
        temp_filename = f"{unique_id}.mmd"
        
        with open(temp_filename, 'w') as f:
            f.write(content)
        
        temp_files[unique_id] = temp_filename
    
    return temp_files

async def render_unified_mermaid_diagrams(inline_blocks: List[Tuple[str, str]], 
                                        external_contents: Dict[str, Tuple[str, str]], 
                                        width: int = 1200, height: int = 800) -> Dict[str, str]:
    """
    Unified rendering function for both inline and external Mermaid diagrams.
    Generates unique image filenames to avoid conflicts and processes all diagrams in a single workflow.
    """
    image_mappings = {}
    total_diagrams = len(inline_blocks) + len(external_contents)
    processed_count = 0
    
    print(f"Processing {total_diagrams} Mermaid diagram(s) ({len(inline_blocks)} inline, {len(external_contents)} external) at {width}x{height}...")
    
    # Process inline Mermaid blocks
    for block_content, unique_id in inline_blocks:
        png_filename = f"{unique_id}.png"
        
        try:
            await mermaid_to_image(block_content, png_filename, width, height)
            image_mappings[unique_id] = png_filename
            processed_count += 1
            print(f"✓ [{processed_count}/{total_diagrams}] Inline diagram: {unique_id} -> {png_filename}")
            
        except Exception as e:
            print(f"✗ [{processed_count + 1}/{total_diagrams}] Error processing inline diagram {unique_id}: {e}")
            print(f"  Continuing with remaining diagrams...")
    
    # Process external .mmd file contents
    for unique_id, (content, alt_text) in external_contents.items():
        png_filename = f"{unique_id}.png"
        
        try:
            await mermaid_to_image(content, png_filename, width, height)
            image_mappings[unique_id] = png_filename
            processed_count += 1
            print(f"✓ [{processed_count}/{total_diagrams}] External diagram: {unique_id} -> {png_filename}")
            
        except Exception as e:
            print(f"✗ [{processed_count + 1}/{total_diagrams}] Error processing external diagram {unique_id}: {e}")
            print(f"  Continuing with remaining diagrams...")
    
    # Summary
    if processed_count == 0:
        print("✗ Failed to process any Mermaid diagrams")
    elif processed_count < total_diagrams:
        print(f"⚠ Successfully processed {processed_count}/{total_diagrams} diagrams")
    else:
        print(f"✓ Successfully processed all {processed_count} diagrams")
    
    return image_mappings

async def render_mermaid_blocks(mmd_files: Dict[str, str], width: int = 1200, height: int = 800) -> Dict[str, str]:
    """
    Legacy function for backward compatibility.
    Render .mmd files to .png and return mapping of id -> image_path
    """
    image_mappings = {}
    total_files = len(mmd_files)
    processed_count = 0
    
    print(f"Processing {total_files} Mermaid diagram(s) at {width}x{height}...")
    
    for unique_id, mmd_filename in mmd_files.items():
        png_filename = f"{unique_id}.png"
        
        try:
            with open(mmd_filename, 'r') as f:
                mermaid_code = f.read()
            
            await mermaid_to_image(mermaid_code, png_filename, width, height)
            image_mappings[unique_id] = png_filename
            processed_count += 1
            print(f"✓ [{processed_count}/{total_files}] Successfully converted {mmd_filename} to {png_filename}")
            
        except Exception as e:
            print(f"✗ [{processed_count + 1}/{total_files}] Error processing {mmd_filename}: {e}")
            print(f"  Continuing with remaining diagrams...")
            # Continue processing other diagrams even if one fails
    
    if processed_count == 0:
        print("✗ Failed to process any Mermaid diagrams")
    elif processed_count < total_files:
        print(f"⚠ Successfully processed {processed_count}/{total_files} diagrams")
    else:
        print(f"✓ Successfully processed all {processed_count} diagrams")
    
    return image_mappings

def replace_mermaid_with_images(markdown_content: str, image_mappings: Dict[str, str]) -> str:
    """Replace Mermaid code blocks with image references in markdown content"""
    modified_content = markdown_content
    
    # Extract blocks again to get them in order for replacement
    mermaid_blocks = extract_mermaid_blocks(markdown_content)
    
    # Replace each mermaid block with corresponding image reference
    for i, (block_content, _) in enumerate(mermaid_blocks):
        # Find the unique_id for this block (they're created in order)
        matching_id = None
        for unique_id, image_path in image_mappings.items():
            if unique_id.endswith(f"_{i}"):
                matching_id = unique_id
                break
        
        if matching_id and matching_id in image_mappings:
            # Create the mermaid block pattern to replace
            mermaid_block_pattern = f"```mermaid\n{re.escape(block_content)}\n```"
            image_reference = f"![Mermaid Diagram]({image_mappings[matching_id]})"
            
            # Replace the first occurrence (since we're processing in order)
            modified_content = re.sub(mermaid_block_pattern, image_reference, modified_content, count=1)
    
    return modified_content

def replace_mermaid_and_mmd_with_images(markdown_content: str, image_mappings: Dict[str, str], 
                                       mermaid_blocks: List[Tuple[str, str]], 
                                       mmd_references: List[Tuple[str, str, str]],
                                       mmd_contents: Dict[str, Tuple[str, str]]) -> str:
    """
    Replace both Mermaid blocks and .mmd file references with image references in markdown content.
    Maintains original document structure and diagram positioning by processing in document order.
    """
    modified_content = markdown_content
    
    # Create a list of all replacements with their positions in the document
    replacements = []
    
    # Find positions of inline Mermaid blocks
    inline_pattern = r'```mermaid\n(.*?)\n```'
    for match in re.finditer(inline_pattern, markdown_content, re.DOTALL):
        block_content = match.group(1).strip()
        start_pos = match.start()
        
        # Find matching unique_id for this block content
        matching_id = None
        for block_content_stored, unique_id in mermaid_blocks:
            if block_content_stored == block_content and unique_id in image_mappings:
                matching_id = unique_id
                break
        
        if matching_id:
            replacements.append({
                'start': start_pos,
                'end': match.end(),
                'original': match.group(0),
                'replacement': f"![Mermaid Diagram]({image_mappings[matching_id]})",
                'type': 'inline'
            })
    
    # Find positions of .mmd file references
    # Pattern matches: ![alt](file.mmd) or ![alt](file.mmd "title")
    mmd_pattern = r'!\[([^\]]*)\]\(([^\s)]+\.mmd)(?:\s+"[^"]*")?\)'
    for match in re.finditer(mmd_pattern, markdown_content):
        alt_text = match.group(1)
        file_path = match.group(2)
        start_pos = match.start()
        
        # Find matching unique_id for this reference
        matching_id = None
        for stored_file_path, stored_alt_text, unique_id in mmd_references:
            if (stored_file_path == file_path.strip() and 
                stored_alt_text == alt_text.strip() and 
                unique_id in image_mappings and 
                unique_id in mmd_contents):
                matching_id = unique_id
                break
        
        if matching_id:
            # Use original alt text if available, otherwise use default
            display_alt_text = alt_text if alt_text else "Mermaid Diagram"
            replacements.append({
                'start': start_pos,
                'end': match.end(),
                'original': match.group(0),
                'replacement': f"![{display_alt_text}]({image_mappings[matching_id]})",
                'type': 'external'
            })
    
    # Sort replacements by position (reverse order to avoid position shifts)
    replacements.sort(key=lambda x: x['start'], reverse=True)
    
    # Apply replacements from end to beginning to maintain positions
    for replacement in replacements:
        modified_content = (
            modified_content[:replacement['start']] + 
            replacement['replacement'] + 
            modified_content[replacement['end']:]
        )
    
    return modified_content

def create_temp_markdown(modified_content: str) -> str:
    """Create temporary markdown file with image references"""
    temp_markdown = f"temp_markdown_{uuid.uuid4().hex[:8]}.md"
    
    with open(temp_markdown, 'w') as f:
        f.write(modified_content)
    
    return temp_markdown

def generate_pdf_from_markdown(temp_markdown_path: str, output_pdf_path: str, has_images: bool = True, 
                             pdf_engine: str = None, margin: str = "1in", include_toc: bool = True) -> bool:
    """Generate PDF using pandoc with enhanced options and fallback engine support"""
    if not os.path.exists(temp_markdown_path):
        print(f"Error: {temp_markdown_path} not found")
        return False
    
    print(f"Generating PDF: {temp_markdown_path} -> {output_pdf_path}")
    
    # Get available dependencies if engine not specified
    if pdf_engine is None:
        dependencies = validate_dependencies()
        pdf_engine = get_available_pdf_engine(dependencies)
        
        if not pdf_engine:
            print("✗ Error: No PDF engines available")
            print_dependency_status(dependencies)
            return False
    
    print(f"Using PDF engine: {pdf_engine}")
    
    try:
        # Verify pandoc is available
        subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
        
        # Create LaTeX header based on engine and requirements
        latex_packages = []
        
        if has_images:
            latex_packages.extend([
                "\\usepackage{float}",
                "\\usepackage{placeins}",
                "\\floatplacement{figure}{H}",
                "\\setkeys{Gin}{width=\\maxwidth,height=\\maxheight,keepaspectratio}"
            ])
        else:
            latex_packages.extend([
                "\\usepackage{float}",
                "\\usepackage{placeins}"
            ])
        
        # Engine-specific optimizations
        if pdf_engine == 'xelatex':
            latex_packages.extend([
                "\\usepackage{fontspec}",  # Better font handling
                "\\usepackage{unicode-math}"  # Unicode math support
            ])
        elif pdf_engine == 'lualatex':
            latex_packages.extend([
                "\\usepackage{fontspec}",  # Better font handling
                "\\usepackage{luacode}"  # Lua integration
            ])
        
        latex_header = "\n".join(latex_packages)
        
        # Build pandoc command
        cmd = [
            'pandoc',
            temp_markdown_path,
            '-o', output_pdf_path,
            f'--pdf-engine={pdf_engine}',
            '-V', f'geometry:margin={margin}',
            '-V', f'header-includes={latex_header}',
            '--standalone'
        ]
        
        # Add TOC if requested
        if include_toc:
            cmd.extend(['--toc', '--toc-depth=3'])
        
        # Execute pandoc with fallback handling
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Successfully generated {output_pdf_path} using {pdf_engine}")
            return True
        else:
            print(f"✗ Error generating PDF with {pdf_engine}: {result.stderr}")
            
            # Try fallback engines if the specified one failed
            if pdf_engine != 'pdflatex':
                print(f"Attempting fallback to pdflatex...")
                return generate_pdf_from_markdown(temp_markdown_path, output_pdf_path, 
                                                has_images, 'pdflatex', margin, include_toc)
            
            return False
            
    except subprocess.CalledProcessError:
        print("✗ Error: Pandoc not found")
        dependencies = validate_dependencies()
        print_dependency_status(dependencies)
        return False
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        return False

def cleanup_temp_files(file_paths: List[str], keep_temp: bool = False) -> None:
    """Clean up all temporary files created during processing"""
    if not file_paths:
        print("No temporary files to clean up")
        return
    
    if keep_temp:
        print(f"Keeping {len(file_paths)} temporary files for debugging:")
        for file_path in file_paths:
            if os.path.exists(file_path):
                print(f"  - {file_path}")
        return
    
    cleaned_count = 0
    total_files = len(file_paths)
    
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                cleaned_count += 1
                print(f"✓ Cleaned up {file_path}")
            else:
                print(f"ℹ File already removed: {file_path}")
        except Exception as e:
            print(f"⚠ Warning: Could not clean up {file_path}: {e}")
    
    if cleaned_count == total_files:
        print(f"✓ Successfully cleaned up all {cleaned_count} temporary files")
    elif cleaned_count > 0:
        print(f"⚠ Cleaned up {cleaned_count}/{total_files} temporary files")
    else:
        print("⚠ No temporary files were cleaned up")

async def convert_markdown_to_pdf(input_markdown: str, output_pdf: str = None, 
                                 pdf_engine: str = None, margin: str = "1in", 
                                 include_toc: bool = True, image_width: int = 1200,
                                 image_height: int = 800, keep_temp: bool = False) -> str:
    """Main function that orchestrates the entire conversion process"""
    if not os.path.exists(input_markdown):
        raise FileNotFoundError(f"Input markdown file not found: {input_markdown}")
    
    # Generate output PDF name if not provided
    if output_pdf is None:
        base_name = os.path.splitext(input_markdown)[0]
        output_pdf = f"{base_name}_output.pdf"
    
    temp_files_to_cleanup = []
    
    try:
        print(f"=== Converting {input_markdown} to PDF ===\n")
        
        # Step 0: Validate dependencies
        print("Step 0: Validating system dependencies...")
        dependencies = check_dependencies_or_exit()
        
        # Get PDF engine if not specified
        if pdf_engine is None:
            pdf_engine = get_available_pdf_engine(dependencies)
        
        print(f"Using PDF engine: {pdf_engine}")
        print(f"PDF options: margin={margin}, toc={include_toc}")
        print(f"Image options: {image_width}x{image_height}")
        print()
        
        # Step 1: Read the markdown file
        print("Step 1: Reading markdown file...")
        with open(input_markdown, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Step 2: Extract Mermaid blocks and detect external .mmd file references
        print("Step 2: Extracting Mermaid code blocks and detecting .mmd file references...")
        mermaid_blocks = extract_mermaid_blocks(markdown_content)
        
        # Get base path for resolving relative .mmd file paths
        base_path = os.path.dirname(os.path.abspath(input_markdown))
        mmd_references = detect_mmd_file_references(markdown_content)
        
        print(f"Found {len(mermaid_blocks)} inline Mermaid block(s)")
        print(f"Found {len(mmd_references)} external .mmd file reference(s)")
        
        if not mermaid_blocks and not mmd_references:
            print("No Mermaid blocks or .mmd file references found. Generating PDF directly from markdown...")
            # Generate PDF directly without processing
            success = generate_pdf_from_markdown(input_markdown, output_pdf, 
                                               has_images=False, pdf_engine=pdf_engine, 
                                               margin=margin, include_toc=include_toc)
            if success:
                print(f"\n✓ PDF generated successfully: {output_pdf}")
                return output_pdf
            else:
                raise Exception("Failed to generate PDF")
        
        # Step 3: Read external .mmd files
        print("Step 3: Reading external .mmd files...")
        mmd_contents = read_mmd_files(mmd_references, base_path)
        
        # Step 4: Unified diagram processing - render both inline and external diagrams
        print("Step 4: Processing unified diagram workflow...")
        image_mappings = await render_unified_mermaid_diagrams(mermaid_blocks, mmd_contents, image_width, image_height)
        temp_files_to_cleanup.extend(image_mappings.values())
        
        if not image_mappings:
            raise Exception("Failed to render any Mermaid diagrams - check syntax and dependencies")
        
        # Step 5: Replace Mermaid blocks and .mmd file references with image references
        print("Step 5: Replacing diagrams with image references (maintaining document structure)...")
        modified_markdown = replace_mermaid_and_mmd_with_images(markdown_content, image_mappings, 
                                                               mermaid_blocks, mmd_references, mmd_contents)
        
        # Step 6: Create temporary markdown file
        print("Step 6: Creating temporary markdown file...")
        temp_markdown_path = create_temp_markdown(modified_markdown)
        temp_files_to_cleanup.append(temp_markdown_path)
        
        # Step 7: Generate PDF
        print("Step 7: Generating PDF...")
        success = generate_pdf_from_markdown(temp_markdown_path, output_pdf, 
                                           has_images=True, pdf_engine=pdf_engine, 
                                           margin=margin, include_toc=include_toc)
        
        if success:
            print(f"\n✓ PDF generated successfully: {output_pdf}")
            return output_pdf
        else:
            raise Exception("Failed to generate PDF")
    
    except Exception as e:
        print(f"\n✗ Error during conversion: {e}")
        raise
    
    finally:
        # Step 8: Clean up temporary files
        print("\nStep 8: Cleaning up temporary files...")
        cleanup_temp_files(temp_files_to_cleanup, keep_temp)

# Legacy functions for backward compatibility
async def process_all_mmd_files():
    """Process all .mmd files in the current directory (legacy function)"""
    mmd_files = glob.glob("*.mmd")
    
    if not mmd_files:
        print("No .mmd files found in current directory")
        return []
    
    processed_files = []
    
    for mmd_file in mmd_files:
        # Generate output filename (replace .mmd with .png)
        output_file = mmd_file.replace('.mmd', '.png')
        
        print(f"Processing {mmd_file} -> {output_file}")
        
        try:
            with open(mmd_file, 'r') as f:
                mermaid_code = f.read()
            
            await mermaid_to_image(mermaid_code, output_file)
            processed_files.append((mmd_file, output_file))
            print(f"✓ Successfully converted {mmd_file} to {output_file}")
            
        except Exception as e:
            print(f"✗ Error processing {mmd_file}: {e}")
    
    return processed_files

def update_markdown_images(markdown_file="design-with-images.md"):
    """Update markdown file to ensure image references are correct (legacy function)"""
    if not os.path.exists(markdown_file):
        print(f"Warning: {markdown_file} not found")
        return False
    
    print(f"Updating image references in {markdown_file}")
    
    with open(markdown_file, 'r') as f:
        content = f.read()
    
    # Update image references to use .png extension
    # Pattern: ![Alt text](filename.png) or ![Alt text](filename.mmd)
    updated_content = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\.mmd\)',
        r'![\1](\2.png)',
        content
    )
    
    # Ensure architecture-diagram and data-flow-diagram references are correct
    updated_content = re.sub(
        r'!\[Architecture Diagram\]\([^)]*\)',
        '![Architecture Diagram](architecture-diagram.png)',
        updated_content
    )
    
    updated_content = re.sub(
        r'!\[Data Flow Diagram\]\([^)]*\)',
        '![Data Flow Diagram](data-flow-diagram.png)',
        updated_content
    )
    
    if content != updated_content:
        with open(markdown_file, 'w') as f:
            f.write(updated_content)
        print(f"✓ Updated image references in {markdown_file}")
        return True
    else:
        print(f"✓ Image references in {markdown_file} are already correct")
        return True

def generate_pdf(markdown_file="design-with-images.md", output_pdf="design-output.pdf"):
    """Generate PDF from markdown using Pandoc (legacy function)"""
    return generate_pdf_from_markdown(markdown_file, output_pdf)

async def run_end_to_end():
    """Run the complete end-to-end process (legacy function)"""
    print("=== Starting End-to-End PDF Generation Process ===\n")
    
    # Step 1: Process all MMD files
    print("Step 1: Converting Mermaid diagrams to images...")
    processed_files = await process_all_mmd_files()
    
    if not processed_files:
        print("No files processed. Exiting.")
        return False
    
    print(f"\nProcessed {len(processed_files)} diagram(s)\n")
    
    # Step 2: Update markdown file
    print("Step 2: Updating markdown file...")
    markdown_updated = update_markdown_images()
    
    if not markdown_updated:
        print("Failed to update markdown file. Exiting.")
        return False
    
    print()
    
    # Step 3: Generate PDF
    print("Step 3: Generating PDF...")
    pdf_generated = generate_pdf()
    
    if pdf_generated:
        print("\n=== End-to-End Process Completed Successfully! ===")
        print("Files generated:")
        for mmd_file, png_file in processed_files:
            print(f"  - {png_file}")
        print(f"  - design-output.pdf")
        return True
    else:
        print("\n=== Process completed with errors ===")
        return False

async def main():
    parser = argparse.ArgumentParser(description='Convert Markdown with inline Mermaid diagrams to PDF')
    parser.add_argument('input', nargs='?', help='Input markdown file')
    parser.add_argument('-o', '--output', help='Output PDF file (optional)')
    
    # PDF Generation Options
    pdf_group = parser.add_argument_group('PDF Generation Options')
    pdf_group.add_argument('--engine', choices=['xelatex', 'lualatex', 'pdflatex'], 
                          help='PDF engine to use (default: auto-detect best available)')
    pdf_group.add_argument('--margin', default='1in', 
                          help='Page margins (default: 1in). Examples: 0.5in, 2cm, 20mm')
    pdf_group.add_argument('--no-toc', action='store_true', 
                          help='Disable table of contents generation')
    pdf_group.add_argument('--toc-depth', type=int, default=3, 
                          help='Table of contents depth (default: 3)')
    
    # Image Processing Options
    image_group = parser.add_argument_group('Image Processing Options')
    image_group.add_argument('--image-width', type=int, default=1200, 
                            help='Mermaid image width in pixels (default: 1200)')
    image_group.add_argument('--image-height', type=int, default=800, 
                            help='Mermaid image height in pixels (default: 800)')
    
    # Utility Options
    util_group = parser.add_argument_group('Utility Options')
    util_group.add_argument('--check-deps', action='store_true', 
                           help='Check system dependencies and exit')
    util_group.add_argument('--keep-temp', action='store_true', 
                           help='Keep temporary files for debugging')
    util_group.add_argument('--verbose', '-v', action='store_true', 
                           help='Enable verbose output')
    
    # Legacy Options (for backward compatibility)
    legacy_group = parser.add_argument_group('Legacy Options')
    legacy_group.add_argument('--single', nargs=2, metavar=('INPUT', 'OUTPUT'),
                             help='Convert single MMD file: --single input.mmd output.png')
    legacy_group.add_argument('--legacy', action='store_true',
                             help='Run legacy end-to-end process')
    
    args = parser.parse_args()
    
    # Handle dependency check
    if args.check_deps:
        print("=== System Dependency Check ===\n")
        dependencies = validate_dependencies()
        print_dependency_status(dependencies)
        
        # Check if system is ready
        missing_required = [name for name, info in dependencies.items() 
                          if info['required'] and info['status'] == 'missing']
        available_engine = get_available_pdf_engine(dependencies)
        
        if missing_required or not available_engine:
            print("✗ System is not ready for PDF conversion")
            sys.exit(1)
        else:
            print("✓ System is ready for PDF conversion")
            sys.exit(0)
    
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
        
    elif args.legacy:
        # Legacy end-to-end mode
        success = await run_end_to_end()
        sys.exit(0 if success else 1)
        
    elif args.input:
        # New unified conversion mode
        try:
            # Set global verbose flag if needed
            if args.verbose:
                print("Verbose mode enabled")
            
            output_pdf = await convert_markdown_to_pdf(
                input_markdown=args.input,
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
            
            if args.keep_temp:
                print("Note: Temporary files were preserved for debugging (--keep-temp)")
            
            sys.exit(0)
        except Exception as e:
            print(f"\n=== Conversion failed ===")
            print(f"Error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    else:
        # No arguments provided, show help
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())