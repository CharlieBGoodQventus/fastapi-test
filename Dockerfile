# syntax=docker/dockerfile:1

# Multi-stage Dockerfile for fast-api-test
# Stage 1: Builder - Install dependencies
FROM python:3.10-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install uv package manager via official install script
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /build

COPY pyproject.toml uv.lock ./

# Configure git to use GitHub token for private dependencies
# Uses BuildKit secret mount - token never baked into image layers
RUN --mount=type=secret,id=API_TOKEN_GITHUB git config --global \
    url."https://$(cat /run/secrets/API_TOKEN_GITHUB)@github.com/".insteadOf \
    "ssh://git@github.com/"

# Install dependencies (frozen lockfile for reproducibility)
RUN uv sync --frozen --no-install-project

# Stage 2: Runtime - Minimal production image
FROM python:3.10-slim AS runner

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    SSL_CERTFILE=/etc/certs/tls.crt \
    SSL_KEYFILE=/etc/certs/tls.key \
    UVICORN_PORT=8443 \
    UVICORN_HOST=0.0.0.0

# Create non-root user with UID 1000 to match Helm security context
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser -s /sbin/nologin -c "Application user" appuser

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder --chown=appuser:appuser /build/.venv /app/.venv

# Copy application source code
COPY --chown=appuser:appuser src/ /app/src/

# Create directories for writable paths
RUN mkdir -p /tmp /var/tmp && \
    chown -R appuser:appuser /tmp /var/tmp

# Switch to non-root user
USER appuser

EXPOSE 8443

# Health check using the /status endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request, ssl; urllib.request.urlopen('https://localhost:8443/status', context=ssl._create_unverified_context())" || exit 1

# Rewrite shebangs to use the libraries in the runner stage
RUN find /app/.venv/bin -type f \
    -exec sed -i "1s|^#!.*python.*$|#!/app/.venv/bin/python|" {} \;

# Start uvicorn with production settings
CMD ["sh", "-c", "exec python -m uvicorn fast_api_test.main:app \
    --host ${UVICORN_HOST} \
    --port ${UVICORN_PORT} \
    --workers ${UVICORN_WORKERS:-$((2 * $(nproc) + 1))} \
    --no-access-log \
    --ssl-keyfile ${SSL_KEYFILE} \
    --ssl-certfile ${SSL_CERTFILE}"]
