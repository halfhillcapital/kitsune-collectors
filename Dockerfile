FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY kitsune/ kitsune/
COPY notebooks/ notebooks/
RUN uv sync --frozen --no-dev

EXPOSE 8011

CMD ["uv", "run", "marimo", "edit", "--host", "0.0.0.0", "--port", "8011", "--no-token", "notebooks/"]
