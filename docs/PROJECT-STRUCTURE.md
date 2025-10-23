# Project Structure

This document describes the organization and purpose of all files in this repository.

## Directory Tree

```
markdown-to-pdf/
├── README.md                                    # Main documentation
├── CHANGELOG.md                                 # Version history
├── LICENSE                                      # MIT License
│
├── Dockerfile                                   # Container definition
├── docker-compose.yml                           # Docker Compose config
├── .dockerignore                                # Docker build exclusions
├── .gitignore                                   # Git exclusions
├── entrypoint.sh                                # Container entry point
├── requirements.txt                             # Python dependencies
│
├── build.sh                                     # Build automation script
│
├── src/                                         # Source code
│   ├── converter.py                             # Core conversion logic
│   └── cli.py                                   # CLI interface & batch processing
│
├── tests/                                       # Test suite
│   └── test_batch.py                            # Batch processing tests
│
├── docs/                                        # Documentation
│   ├── GETTING-STARTED.md                       # Step-by-step setup guide
│   ├── QUICK-REFERENCE.md                       # Command reference card
│   ├── DOCKER-USAGE.md                          # Docker-specific details
│   ├── DEPLOYMENT.md                            # Production deployment guide
│   ├── CONTRIBUTING.md                          # Contribution guidelines
│   ├── PROJECT-STRUCTURE.md                     # This file
│   └── REPOSITORY-SETUP.md                      # Repository setup guide
│
└── examples/                                    # Example files
    ├── README.md                                # Examples documentation
    ├── convert-examples.sh                      # Convert all examples script
    ├── simple-example.md                        # Inline diagrams example
    ├── external-diagrams-example.md             # External .mmd example
    └── diagrams/                                # External diagram files
        ├── architecture.mmd                     # Architecture diagram
        └── workflow.mmd                         # Workflow diagram
```

## Core Files

### Application Code

#### `src/converter.py`
- **Purpose**: Core conversion logic
- **Contains**:
  - Mermaid diagram rendering
  - Markdown parsing
  - PDF generation
  - Dependency validation
  - File handling utilities
- **Used by**: CLI module
- **Dependencies**: playwright, pandoc, LaTeX

#### `src/cli.py`
- **Purpose**: Command-line interface and batch processing
- **Contains**:
  - File discovery (recursive/non-recursive)
  - Batch processing logic
  - Enhanced argument parsing
  - Progress tracking
  - Error handling for multiple files
- **Imports**: Core converter functions
- **Entry point**: Main CLI interface

#### `requirements.txt`
- **Purpose**: Python package dependencies
- **Contains**:
  - playwright>=1.40.0 (Mermaid rendering)
  - Standard library modules documented
- **Used by**: Dockerfile pip install

## Container Configuration

### `Dockerfile`
- **Purpose**: Container image definition
- **Stages**: Single-stage build
- **Base**: python:3.11-slim
- **Installs**:
  - System packages (pandoc, LaTeX engines)
  - Python dependencies
  - Playwright browsers
- **Size**: ~2GB (complete LaTeX distribution)
- **Workdir**: /workspace

### `entrypoint.sh`
- **Purpose**: Container entry point script
- **Functions**:
  - Usage information display
  - Help text
  - Argument forwarding to Python script
- **Permissions**: Executable (chmod +x)

### `docker-compose.yml`
- **Purpose**: Simplified container management
- **Defines**:
  - Service configuration
  - Volume mounts
  - Working directory
- **Usage**: Alternative to docker run commands

### `.dockerignore`
- **Purpose**: Optimize Docker build context
- **Excludes**:
  - Git files
  - Generated PDFs/PNGs
  - Python cache
  - Documentation (not needed in container)
  - Test files

## Build and Test Scripts

### `build.sh`
- **Purpose**: Automated container build
- **Functions**:
  - Builds Docker image
  - Tags as markdown-pdf-converter:latest
  - Displays usage examples
  - Shows alias creation command
- **Permissions**: Executable

### `examples/convert-examples.sh`
- **Purpose**: Convert example files to PDF
- **Functions**:
  - Checks Docker availability
  - Verifies image exists
  - Converts all example markdown files
  - Generates PDFs in examples directory
  - Shows conversion results
  - Displays usage examples
- **Permissions**: Executable
- **Usage**: Run from examples directory

### `tests/test_batch.py`
- **Purpose**: Automated testing
- **Tests**:
  - File discovery functionality
  - Recursive/non-recursive search
  - Batch processing structure
  - Edge cases
- **Usage**: `python tests/test_batch.py`

## Documentation

### User Documentation

#### `README.md`
- **Audience**: All users
- **Contains**:
  - Feature overview
  - Quick start guide
  - Usage examples
  - Command reference
  - Troubleshooting
  - CI/CD integration examples
  - Links to extended documentation
- **Length**: Comprehensive (~500 lines)

### Extended Documentation (`docs/`)

#### `docs/GETTING-STARTED.md`
- **Audience**: New users
- **Contains**:
  - Step-by-step setup
  - First conversion tutorial
  - Common usage patterns
  - Alias creation
  - Project organization tips
  - Troubleshooting basics
- **Length**: Detailed tutorial (~400 lines)

#### `docs/QUICK-REFERENCE.md`
- **Audience**: Experienced users
- **Contains**:
  - Command cheat sheet
  - All options listed
  - Common workflows
  - Quality presets
  - Quick troubleshooting
- **Length**: Concise reference (~200 lines)

#### `docs/DOCKER-USAGE.md`
- **Audience**: Docker users
- **Contains**:
  - Container details
  - Advanced Docker usage
  - Volume mounting
  - Networking
  - Performance tuning
- **Length**: Docker-focused (~300 lines)

#### `docs/DEPLOYMENT.md`
- **Audience**: DevOps/Deployment
- **Contains**:
  - Production deployment strategies
  - Registry distribution
  - CI/CD integration
  - Kubernetes examples
  - Monitoring and logging
  - Security considerations
- **Length**: Production guide (~400 lines)

#### `docs/CONTRIBUTING.md`
- **Audience**: Contributors
- **Contains**:
  - Development setup
  - Code style guidelines
  - Testing requirements
  - PR process
  - Commit message format
  - Bug report template
- **Length**: Contribution guide (~300 lines)

#### `CHANGELOG.md` (root)
- **Audience**: All users
- **Contains**:
  - Version history
  - Release notes
  - Breaking changes
  - Planned features
- **Format**: Keep a Changelog standard

#### `docs/PROJECT-STRUCTURE.md`
- **Audience**: Developers/Contributors
- **Contains**: This document
- **Purpose**: Understand repository organization

#### `docs/REPOSITORY-SETUP.md`
- **Audience**: Maintainers
- **Contains**: GitHub setup instructions
- **Purpose**: Guide for setting up the repository

## Examples

### `examples/`
- **Purpose**: Demonstrate features
- **Contains**:
  - Working example files
  - Sample diagrams
  - Documentation

#### `examples/README.md`
- **Purpose**: Examples documentation
- **Contains**:
  - File descriptions
  - Conversion commands
  - Expected outputs
  - Customization examples

#### `examples/simple-example.md`
- **Purpose**: Basic inline diagrams
- **Contains**:
  - Flowchart example
  - Sequence diagram example
  - Simple markdown content
- **Demonstrates**: Inline Mermaid blocks

#### `examples/external-diagrams-example.md`
- **Purpose**: External file references
- **Contains**:
  - References to .mmd files
  - Mixed inline and external
  - Documentation about external files
- **Demonstrates**: External .mmd references

#### `examples/diagrams/architecture.mmd`
- **Purpose**: Reusable architecture diagram
- **Type**: Mermaid flowchart
- **Shows**: Multi-layer system architecture

#### `examples/diagrams/workflow.mmd`
- **Purpose**: Reusable workflow diagram
- **Type**: Mermaid flowchart
- **Shows**: Authentication/authorization flow

## Configuration Files

### `.gitignore`
- **Purpose**: Git exclusions
- **Excludes**:
  - Python cache
  - Generated PDFs/PNGs
  - Temporary files
  - IDE files
  - OS files
- **Includes**: Option to keep example PDFs

### `LICENSE`
- **Type**: MIT License
- **Purpose**: Open source licensing
- **Allows**: Free use, modification, distribution

## File Relationships

```
build.sh
  └─> Dockerfile
       ├─> requirements.txt
       ├─> src/converter.py
       ├─> src/cli.py
       └─> entrypoint.sh
            └─> src/cli.py
                 └─> src/converter.py

examples/convert-examples.sh
  └─> markdown-pdf-converter (container)
       └─> examples/*.md

tests/test_batch.py
  └─> src/cli.py
       └─> src/converter.py
```

## Usage Flow

1. **Build**: `./build.sh` → Creates container
2. **Run**: `docker run ...` → Executes entrypoint.sh
3. **Process**: entrypoint.sh → Calls batch processor
4. **Convert**: Batch processor → Uses core converter
5. **Output**: PDF files generated in workspace

## Maintenance

### Regular Updates
- **Dockerfile**: Update base image, dependencies
- **requirements.txt**: Update Python packages
- **CHANGELOG.md**: Document changes
- **README.md**: Update for new features
- **docs/**: Keep documentation in sync with code

### Version Control
- Tag releases: `git tag v1.0.0`
- Update CHANGELOG for each release
- Keep documentation in sync with code

### Testing
- Run `python tests/test_batch.py` before releases
- Test with example files
- Verify Docker build succeeds
- Check all documentation links

## Size Information

### Repository Size
- **Source code** (`src/`): ~50 KB (Python scripts)
- **Documentation** (`docs/` + root): ~100 KB (Markdown files)
- **Examples** (`examples/`): ~5 KB (Sample files)
- **Tests** (`tests/`): ~5 KB
- **Total**: ~160 KB (excluding container)

### Container Size
- **Base image**: ~150 MB
- **System packages**: ~1.5 GB (LaTeX)
- **Python packages**: ~200 MB
- **Playwright**: ~150 MB
- **Total**: ~2 GB

## Dependencies

### System Dependencies (in container)
- pandoc
- texlive-xetex
- texlive-luatex
- texlive-latex-base
- texlive-latex-recommended
- texlive-latex-extra
- texlive-fonts-recommended
- texlive-pictures
- texlive-science

### Python Dependencies
- playwright>=1.40.0
- Standard library (no additional packages)

### Runtime Dependencies
- Docker (for users)
- Chromium (installed by Playwright)

## Future Additions

Planned files/directories:
- `.github/workflows/` - GitHub Actions CI/CD
- `k8s/` - Kubernetes manifests
- `web/` - Web service wrapper
- `config/` - Configuration templates
- Additional tests in `tests/`

---

**Last Updated**: 2024-10-23
**Version**: 1.0.0