# Deployment Guide: Containerized Markdown to PDF Converter

This guide covers deploying the containerized markdown to PDF converter for production use.

## What We've Built

A Docker container that:
- ✅ Includes all system dependencies (pandoc, LaTeX, Chromium)
- ✅ Supports batch processing of multiple files and folders
- ✅ Handles complex file structures with external .mmd references
- ✅ Provides a clean CLI interface
- ✅ Works across all platforms with Docker

## Files Created

### Core Application
- `src/cli.py` - Command-line interface with batch processing
- `src/converter.py` - Core conversion logic (imported by CLI)
- `requirements.txt` - Python dependencies

### Container Configuration
- `Dockerfile` - Multi-stage build with all dependencies
- `entrypoint.sh` - Container entry point with usage help
- `.dockerignore` - Optimized build context
- `docker-compose.yml` - Easy container management

### Build and Documentation
- `build.sh` - Automated build script
- `README.md` - Main documentation
- `docs/DEPLOYMENT.md` - This deployment guide
- `tests/test_batch.py` - Batch functionality tests

## Quick Deployment

### 1. Build the Container

```bash
# Make build script executable and run
chmod +x build.sh
./build.sh
```

### 2. Test Basic Functionality

```bash
# Test with existing files
docker run --rm -v $(pwd):/workspace markdown-pdf-converter README.md

# Check dependencies
docker run --rm markdown-pdf-converter --check-deps
```

### 3. Create User-Friendly Alias

```bash
# Add to ~/.bashrc or ~/.zshrc
alias md2pdf='docker run --rm -v $(pwd):/workspace markdown-pdf-converter'

# Usage becomes simple:
md2pdf README.md
md2pdf --folder docs/
md2pdf *.md
```

## Production Deployment Options

### Option 1: Docker Hub Distribution

```bash
# Tag for Docker Hub
docker tag markdown-pdf-converter:latest yourusername/markdown-pdf-converter:latest

# Push to Docker Hub
docker push yourusername/markdown-pdf-converter:latest

# Users can then run:
docker run --rm -v $(pwd):/workspace yourusername/markdown-pdf-converter README.md
```

### Option 2: GitHub Container Registry

```bash
# Tag for GitHub Container Registry
docker tag markdown-pdf-converter:latest ghcr.io/yourusername/markdown-pdf-converter:latest

# Push to GHCR
docker push ghcr.io/yourusername/markdown-pdf-converter:latest
```

### Option 3: Private Registry

```bash
# Tag for private registry
docker tag markdown-pdf-converter:latest your-registry.com/markdown-pdf-converter:latest

# Push to private registry
docker push your-registry.com/markdown-pdf-converter:latest
```

### Option 4: Standalone Executable Distribution

Create a wrapper script that users can download:

```bash
#!/bin/bash
# md2pdf - Wrapper script for containerized converter

IMAGE="yourusername/markdown-pdf-converter:latest"

# Pull image if not present
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
    echo "Pulling markdown-pdf-converter..."
    docker pull "$IMAGE"
fi

# Run converter with mounted current directory
docker run --rm -v "$(pwd):/workspace" "$IMAGE" "$@"
```

## CI/CD Integration Examples

### GitHub Actions

```yaml
name: Generate Documentation
on: [push, pull_request]

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Generate PDFs
        run: |
          docker run --rm -v ${{ github.workspace }}:/workspace \
            yourusername/markdown-pdf-converter:latest \
            --output-dir dist/pdfs/ docs/*.md
      
      - name: Upload PDFs
        uses: actions/upload-artifact@v3
        with:
          name: documentation-pdfs
          path: dist/pdfs/
```

### GitLab CI

```yaml
generate-docs:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker run --rm -v $PWD:/workspace 
        yourusername/markdown-pdf-converter:latest 
        --output-dir dist/pdfs/ docs/*.md
  artifacts:
    paths:
      - dist/pdfs/
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Generate Documentation') {
            steps {
                sh '''
                    docker run --rm -v $PWD:/workspace \
                        yourusername/markdown-pdf-converter:latest \
                        --output-dir dist/pdfs/ docs/*.md
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'dist/pdfs/*.pdf', fingerprint: true
        }
    }
}
```

## Web Service Deployment (Future Enhancement)

The containerized CLI can be easily extended to a web service:

### FastAPI Web Service

```python
# web_service.py (future enhancement)
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import tempfile
import os

app = FastAPI()

@app.post("/convert")
async def convert_markdown(file: UploadFile = File(...)):
    # Save uploaded file
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    # Convert using existing converter
    # ... conversion logic ...
    
    return FileResponse(pdf_path, filename="output.pdf")
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml (future enhancement)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: markdown-converter
spec:
  replicas: 3
  selector:
    matchLabels:
      app: markdown-converter
  template:
    metadata:
      labels:
        app: markdown-converter
    spec:
      containers:
      - name: converter
        image: yourusername/markdown-pdf-converter:latest
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

## Performance Considerations

### Container Optimization
- **Image size**: ~2GB (necessary for complete LaTeX distribution)
- **Memory usage**: 1-2GB recommended for complex documents
- **CPU usage**: Scales with number of Mermaid diagrams

### Scaling Strategies
1. **Horizontal scaling**: Multiple container instances
2. **Batch processing**: Process multiple files per container run
3. **Resource limits**: Set appropriate memory/CPU limits
4. **Caching**: Cache container images locally

## Security Considerations

### Container Security
- Runs as non-root user
- No network access required (after initial setup)
- Only accesses mounted workspace directory
- No persistent storage in container

### Input Validation
- Validates file extensions
- Checks file existence before processing
- Handles malformed Mermaid syntax gracefully

## Monitoring and Logging

### Basic Monitoring

```bash
# Monitor container resource usage
docker stats

# View container logs
docker logs <container_id>

# Health check
docker run --rm markdown-pdf-converter --check-deps
```

### Production Monitoring

```yaml
# docker-compose with monitoring
version: '3.8'
services:
  markdown-converter:
    image: markdown-pdf-converter:latest
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

## Troubleshooting

### Common Issues

1. **Permission errors**: Use `--user $(id -u):$(id -g)` flag
2. **Memory issues**: Increase Docker memory limit
3. **Large files**: Reduce image dimensions with `--image-width` and `--image-height`
4. **Path issues**: Ensure proper volume mounting

### Debug Mode

```bash
# Interactive debugging
docker run --rm -it -v $(pwd):/workspace \
  --entrypoint /bin/bash markdown-pdf-converter

# Verbose output with temp files
docker run --rm -v $(pwd):/workspace markdown-pdf-converter \
  --verbose --keep-temp README.md
```

## Next Steps

1. **Test thoroughly** with your specific markdown files
2. **Choose deployment method** (Docker Hub, private registry, etc.)
3. **Set up CI/CD integration** if needed
4. **Consider web service** for broader accessibility
5. **Monitor usage** and optimize as needed

## Support and Maintenance

- **Updates**: Rebuild container when dependencies change
- **Security**: Regular base image updates
- **Monitoring**: Track conversion success rates and performance
- **Backup**: Ensure important markdown files are version controlled

The containerized solution provides a solid foundation that can be deployed anywhere Docker runs, with the flexibility to extend into web services or integrate into larger systems as needed.