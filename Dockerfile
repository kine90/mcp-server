FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv for fast Python package management
RUN pip install uv && adduser --disabled-password --gecos "" appuser

# Copy dependency files and README (required by pyproject.toml)
COPY pyproject.toml uv.lock README.md ./

# Copy source code first (needed for build)
COPY meraki_mcp/ ./meraki_mcp/

# Install dependencies
RUN uv sync --frozen

# Fix permissions for appuser
RUN chown -R appuser:appuser /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

USER appuser

# Run the MCP server using FastMCP CLI
CMD ["uv", "run", "fastmcp", "run", "meraki_mcp/main.py:mcp"]
