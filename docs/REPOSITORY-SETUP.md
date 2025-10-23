# Repository Setup Guide

This guide helps you set up this project as a new GitHub repository.

## Initial Repository Setup

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `markdown-to-pdf` (or `mermaid-markdown-to-pdf`)
3. Description: "Containerized tool for converting Markdown with Mermaid diagrams to PDF"
4. Choose: Public or Private
5. **Do NOT** initialize with README, .gitignore, or license (we have these)

### 2. Initialize Local Repository

```bash
cd markdown-to-pdf

# Initialize git (if not already initialized)
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Containerized Mermaid Markdown to PDF converter"

# Add remote (replace with your repository URL)
git remote add origin https://github.com/yourusername/markdown-to-pdf.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Repository Configuration

### Topics/Tags

Add these topics to your GitHub repository for discoverability:

- `markdown`
- `pdf`
- `mermaid`
- `docker`
- `converter`
- `documentation`
- `pandoc`
- `latex`
- `diagrams`
- `batch-processing`

### About Section

**Description:**
```
Containerized tool for converting Markdown files with Mermaid diagrams to professional PDFs. Supports batch processing, external diagram files, and zero local installation.
```

**Website:** (if you have one)

### Repository Settings

#### General
- ✅ Enable Issues
- ✅ Enable Discussions (optional)
- ✅ Enable Projects (optional)
- ✅ Enable Wiki (optional)

#### Features
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date

## README Badges (Optional)

Add these badges to the top of README.md:

```markdown
# Mermaid Markdown to PDF Converter

[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/yourusername/mermaid-markdown-to-pdf/graphs/commit-activity)
```

## GitHub Actions (Optional)

Create `.github/workflows/build-test.yml`:

```yaml
name: Build and Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python tests/test_batch.py
    
    - name: Build Docker image
      run: |
        docker build -t markdown-pdf-converter:test .
    
    - name: Test Docker image
      run: |
        docker run --rm markdown-pdf-converter:test --check-deps
    
    - name: Test conversion
      run: |
        docker run --rm -v ${{ github.workspace }}:/workspace \
          markdown-pdf-converter:test examples/simple-example.md
```

## Release Process

### Creating a Release

1. **Update CHANGELOG.md**
   ```markdown
   ## [1.0.0] - 2024-10-23
   ### Added
   - Initial release
   ```

2. **Tag the release**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

3. **Create GitHub Release**
   - Go to Releases → Draft a new release
   - Choose tag: v1.0.0
   - Release title: "v1.0.0 - Initial Release"
   - Description: Copy from CHANGELOG.md
   - Attach any binaries (if applicable)
   - Publish release

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes (2.0.0)
- **MINOR**: New features, backward compatible (1.1.0)
- **PATCH**: Bug fixes (1.0.1)

## Docker Hub Setup (Optional)

### 1. Create Docker Hub Account

Sign up at [Docker Hub](https://hub.docker.com/)

### 2. Create Repository

- Repository name: `markdown-pdf-converter`
- Visibility: Public or Private
- Description: Same as GitHub

### 3. Push to Docker Hub

```bash
# Login
docker login

# Tag image
docker tag markdown-pdf-converter:latest yourusername/markdown-pdf-converter:latest
docker tag markdown-pdf-converter:latest yourusername/markdown-pdf-converter:1.0.0

# Push
docker push yourusername/markdown-pdf-converter:latest
docker push yourusername/markdown-pdf-converter:1.0.0
```

### 4. Update Documentation

Update README.md with Docker Hub instructions:

```markdown
## Quick Start

```bash
# Pull from Docker Hub
docker pull yourusername/markdown-pdf-converter:latest

# Use directly
docker run --rm -v $(pwd):/workspace \
  yourusername/markdown-pdf-converter:latest README.md
```
```

## GitHub Container Registry (Alternative)

### 1. Create Personal Access Token

- Settings → Developer settings → Personal access tokens
- Generate new token with `write:packages` scope

### 2. Login to GHCR

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u yourusername --password-stdin
```

### 3. Push to GHCR

```bash
# Tag
docker tag markdown-pdf-converter:latest \
  ghcr.io/yourusername/markdown-pdf-converter:latest

# Push
docker push ghcr.io/yourusername/markdown-pdf-converter:latest
```

## Documentation Website (Optional)

### GitHub Pages

1. Create `docs/` directory
2. Add documentation files
3. Enable GitHub Pages in repository settings
4. Choose source: `main` branch, `/docs` folder

### Alternative: README-based

Keep all documentation in markdown files in the repository root (current approach).

## Community Files

### Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear description of the bug.

**To Reproduce**
Steps to reproduce the behavior.

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Docker version: [e.g., 24.0.0]

**Additional context**
Any other relevant information.
```

Create `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other approaches you've thought about.

**Additional context**
Any other relevant information.
```

### Pull Request Template

Create `.github/pull_request_template.md`:

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] All tests pass

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented)
```

## Maintenance Schedule

### Regular Tasks

**Weekly:**
- Review and respond to issues
- Review pull requests
- Check for security updates

**Monthly:**
- Update dependencies
- Review and update documentation
- Check Docker base image updates

**Quarterly:**
- Major version updates
- Feature planning
- Performance optimization review

## Marketing and Promotion

### Where to Share

1. **Reddit**
   - r/docker
   - r/programming
   - r/opensource
   - r/devops

2. **Dev.to**
   - Write tutorial article
   - Share use cases

3. **Hacker News**
   - Show HN post

4. **Twitter/X**
   - Tweet with hashtags: #docker #markdown #opensource

5. **Product Hunt**
   - Launch when stable

### Blog Post Ideas

- "Converting Markdown with Mermaid Diagrams to PDF"
- "Containerizing Documentation Tools"
- "Batch Processing Markdown Files with Docker"
- "Zero-Installation Documentation Generation"

## Support Channels

Set up support channels:

1. **GitHub Issues**: Bug reports and feature requests
2. **GitHub Discussions**: Questions and community
3. **Email**: For private inquiries (optional)
4. **Discord/Slack**: Community chat (optional)

## Analytics (Optional)

Track usage:
- GitHub Stars
- Docker Hub pulls
- Issue/PR activity
- Documentation views

## Checklist

Before making repository public:

- [ ] All documentation reviewed
- [ ] Examples tested
- [ ] Build script works
- [ ] Docker image builds successfully
- [ ] Tests pass
- [ ] LICENSE file present
- [ ] README.md complete
- [ ] CONTRIBUTING.md present
- [ ] .gitignore configured
- [ ] Repository description set
- [ ] Topics/tags added
- [ ] Issues enabled
- [ ] Security policy added (optional)

## Next Steps

1. ✅ Initialize repository
2. ✅ Push initial commit
3. ⬜ Add badges to README
4. ⬜ Set up GitHub Actions (optional)
5. ⬜ Create first release
6. ⬜ Push to Docker Hub (optional)
7. ⬜ Add issue templates
8. ⬜ Share with community
9. ⬜ Monitor and respond to feedback
10. ⬜ Plan next features

---

**Ready to share your project with the world!** 🚀