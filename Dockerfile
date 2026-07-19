FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    RAG_HOST=0.0.0.0 \
    RAG_PORT=8004

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY migrations ./migrations

RUN pip install .

EXPOSE 8004

CMD ["uvicorn", "gitflame_coderag.api.app:app", "--host", "0.0.0.0", "--port", "8004"]
