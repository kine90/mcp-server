FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv for fast Python package management
RUN pip install uv

# Copy dependency files and README (required by pyproject.toml)
COPY pyproject.toml uv.lock README.md ./

# Copy source code first (needed for build)
COPY meraki_mcp/ ./meraki_mcp/

# Install dependencies
RUN uv sync --frozen

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Selent integration removed

EXPOSE 8000

# Run the MCP server
CMD ["uv", "run", "python", "-m", "meraki_mcp.main"] 