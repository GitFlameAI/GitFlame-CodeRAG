FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    RAG_HOST=0.0.0.0 \
    RAG_PORT=8004

WORKDIR /app

COPY pyproject.toml README.md ./

RUN pip install --index-url https://download.pytorch.org/whl/cpu "torch>=2.12,<2.13" \
    && pip install \
        "ast-grep-py>=0.44.1" "fastapi>=0.115" "numpy>=2.0" \
        "pgvector>=0.3" "psycopg[binary]>=3.2" "pydantic>=2.8" \
        "pyyaml>=6.0" "rank-bm25>=0.2.2" "sentence-transformers>=3.0" \
        "sqlalchemy>=2.0" "transformers>=4.45,<4.46" "uvicorn[standard]>=0.30"

COPY src ./src
COPY migrations ./migrations

RUN pip install --no-deps .

EXPOSE 8004

CMD ["uvicorn", "gitflame_coderag.api.app:app", "--host", "0.0.0.0", "--port", "8004"]
