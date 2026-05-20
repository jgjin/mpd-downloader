# since we are using .python-version 3.11
FROM python:3.11-slim

# installs minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# sets working directory to /app by convention
WORKDIR /app

# installs uv dependencies before copying application code
COPY --from=ghcr.io/astral-sh/uv:0.11.15 /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

# downloads, verifies, and exposes Shaka Packager
ARG TARGETARCH
RUN if [ "$TARGETARCH" = "arm64" ]; then \
        curl -L https://github.com/shaka-project/shaka-packager/releases/download/v3.7.2/packager-linux-arm64 -o /usr/local/bin/packager; \
    else \
        curl -L https://github.com/shaka-project/shaka-packager/releases/download/v3.7.2/packager-linux-x64 -o /usr/local/bin/packager; \
    fi && \
    chmod +x /usr/local/bin/packager
RUN /usr/local/bin/packager --version
ENV SHAKA_PACKAGER_PATH=/usr/local/bin/packager

# copies rest of application code
COPY . ./

CMD ["uv", "run", "--no-dev", "run_worker.py"]
