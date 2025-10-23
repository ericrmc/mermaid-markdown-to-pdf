# Contributing to Mermaid Markdown to PDF Converter

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new features
- 🧪 Write tests
- 📦 Improve Docker configuration

## Getting Started

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/mermaid-markdown-to-pdf.git
   cd mermaid-markdown-to-pdf
   ```

2. **Build the container**
   ```bash
   ./build.sh
   ```

3. **Run tests**
   ```bash
   python test-batch.py
   ```

4. **Test with examples**
   ```bash
   cd examples
   ./convert-examples.sh
   ```

### Development Workflow

1. Create a new branch for your feature/fix
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test your changes thoroughly
   ```bash
   # Test basic functionality
   docker run --rm -v $(pwd):/workspace markdown-pdf-converter examples/*.md
   
   # Test with verbose output
   docker run --rm -v $(pwd):/workspace markdown-pdf-converter --verbose examples/simple-example.md
   
   # Run automated tests
   python tests/test_batch.py
   ```

4. Commit your changes
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. Push to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

## Code Style

### Python Code
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Add type hints where appropriate

Example:
```python
def process_markdown_file(input_path: str, output_path: str = None) -> str:
    """
    Process a markdown file and convert it to PDF.
    
    Args:
        input_path: Path to input markdown file
        output_path: Optional path for output PDF
        
    Returns:
        Path to generated PDF file
    """
    # Implementation
    pass
```

### Shell Scripts
- Use `#!/bin/bash` shebang
- Add comments for complex operations
- Use `set -e` for error handling
- Quote variables: `"$variable"`

### Docker
- Keep Dockerfile organized with comments
- Minimize layer count where possible
- Clean up in the same layer to reduce image size
- Use multi-stage builds when appropriate

## Testing

### Manual Testing Checklist

Before submitting a PR, test:

- [ ] Single file conversion
- [ ] Multiple file conversion
- [ ] Folder processing (recursive and non-recursive)
- [ ] External .mmd file references
- [ ] Mixed inline and external diagrams
- [ ] Custom output directories
- [ ] Various command-line options
- [ ] Error handling for missing files
- [ ] Error handling for invalid Mermaid syntax

### Automated Tests

Add tests for new functionality:

```python
def test_new_feature():
    """Test description"""
    # Setup
    # Execute
    # Assert
    pass
```

Run tests:
```bash
python tests/test_batch.py
```

## Documentation

### When to Update Documentation

Update documentation when you:
- Add new features
- Change existing behavior
- Add new command-line options
- Fix bugs that affect usage
- Improve performance significantly

### Documentation Files

- **README.md**: Main documentation, feature overview
- **GETTING-STARTED.md**: Step-by-step guide for new users
- **DOCKER-USAGE.md**: Docker-specific details
- **DEPLOYMENT.md**: Production deployment information
- **examples/README.md**: Example usage documentation

### Documentation Style

- Use clear, concise language
- Include code examples
- Add command output examples where helpful
- Use proper markdown formatting
- Test all commands before documenting them

## Commit Messages

Write clear commit messages:

### Format
```
<type>: <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

Good commit messages:
```
feat: add support for custom TOC depth

Added --toc-depth option to allow users to control the depth
of the table of contents in generated PDFs.

Closes #123
```

```
fix: resolve path resolution for external .mmd files

Fixed issue where relative paths were not correctly resolved
when markdown files were in subdirectories.

Fixes #456
```

## Pull Request Process

1. **Update documentation** for any user-facing changes

2. **Add tests** for new functionality

3. **Ensure all tests pass**
   ```bash
   python test-batch.py
   ```

4. **Update CHANGELOG** (if exists) with your changes

5. **Create Pull Request** with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to related issues
   - Screenshots/examples if applicable

6. **Respond to review feedback** promptly

## Reporting Bugs

### Before Reporting

1. Check existing issues to avoid duplicates
2. Test with the latest version
3. Try with `--verbose` flag for detailed output
4. Check if it's a Docker/system issue

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Create file with content...
2. Run command...
3. See error...

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., Ubuntu 22.04, macOS 13, Windows 11]
- Docker version: [e.g., 24.0.0]
- Container version/commit: [e.g., latest, abc123]

**Additional Context**
- Command used: `docker run ...`
- Verbose output: (if applicable)
- Sample files: (if applicable)
```

## Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How you think it should work

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Any other relevant information
```

## Code Review Process

### For Contributors

- Be open to feedback
- Respond to comments promptly
- Make requested changes or explain why not
- Keep discussions professional and constructive

### For Reviewers

- Be respectful and constructive
- Explain the reasoning behind suggestions
- Approve when ready or request specific changes
- Test the changes if possible

## Development Tips

### Testing Changes Without Rebuilding

Mount your local code into the container:

```bash
docker run --rm -v $(pwd):/workspace \
  -v $(pwd)/src/converter.py:/app/converter.py \
  -v $(pwd)/src/cli.py:/app/cli.py \
  markdown-pdf-converter examples/simple-example.md
```

### Debugging

Interactive shell:
```bash
docker run --rm -it -v $(pwd):/workspace \
  --entrypoint /bin/bash markdown-pdf-converter
```

Keep temporary files:
```bash
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --keep-temp --verbose examples/simple-example.md
```

### Performance Testing

Test with large files:
```bash
# Create large test file
for i in {1..100}; do cat examples/simple-example.md >> large-test.md; done

# Time the conversion
time docker run --rm -v $(pwd):/workspace markdown-pdf-converter large-test.md
```

## Questions?

- Open an issue for questions
- Check existing documentation
- Look at example files
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better for everyone. Thank you for taking the time to contribute! 🎉