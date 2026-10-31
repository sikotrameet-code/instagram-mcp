# Instagram MCP Server - Remote HTTP deployment

FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

FROM python:3.12-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/

RUN mkdir -p logs cache && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.http_server:app --host 0.0.0.0 --port ${PORT:-8000}"]
