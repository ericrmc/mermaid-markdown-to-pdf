# Multi-stage build for optimized container size
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Pandoc for markdown to PDF conversion
    pandoc \
    # LaTeX engines for PDF generation (XeLaTeX recommended)
    texlive-xetex \
    texlive-luatex \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    # Additional packages for better PDF output
    texlive-pictures \
    texlive-science \
    # SVG support for LaTeX (optional fallback)
    librsvg2-bin \
    # Clean up to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium --with-deps

# Copy application files
COPY src/converter.py .
COPY src/cli.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Create workspace directory for mounted files
RUN mkdir -p /workspace
WORKDIR /workspace

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]