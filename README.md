# AI Knowledge Assistant

A backend-first retrieval-augmented knowledge assistant built with FastAPI.

Users can ingest text documents, search them semantically with a lightweight TF-IDF retrieval layer, and ask questions through a REST API. The architecture is intentionally modular so the retrieval and answer-generation components can later be swapped for production vector databases and LLM providers.

## Why This Project

This project demonstrates the skills commonly requested in early-career SWE, AI engineering, and forward-deployed engineering roles:

- REST API design
- backend architecture
- persistent data storage
- retrieval / RAG fundamentals
- testing and error handling
- Dockerization
- database-backed application development
- clean separation of concerns

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite locally / PostgreSQL-compatible via `DATABASE_URL`
- scikit-learn TF-IDF retrieval
- Pydantic
- pytest
- Docker

## Architecture

```text
Client
  |
  v
FastAPI REST API
  |
  +--> SQLAlchemy --> SQLite / PostgreSQL
  |
  +--> Retriever --> TF-IDF similarity search
  |
  +--> Answer Service --> context-grounded response
```

## API Endpoints

- `GET /health` — health check
- `POST /documents` — ingest a document
- `GET /documents` — list ingested documents
- `GET /search?q=...` — retrieve the most relevant documents
- `POST /ask` — retrieve context and generate a grounded answer

Interactive documentation is available at `/docs`.

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Example

Ingest a document:

```bash
curl -X POST http://127.0.0.1:8000/documents   -H "Content-Type: application/json"   -d '{"title":"FastAPI","content":"FastAPI is a Python framework for building APIs."}'
```

Ask a question:

```bash
curl -X POST http://127.0.0.1:8000/ask   -H "Content-Type: application/json"   -d '{"question":"What is FastAPI?","top_k":3}'
```

## Run Tests

```bash
pytest -q
```

## Docker

```bash
docker build -t ai-knowledge-assistant .
docker run -p 8000:8000 ai-knowledge-assistant
```

## Engineering Decisions

The first version uses TF-IDF rather than an external embedding API so the repository is fully runnable without paid credentials. The `Retriever` and `AnswerService` layers are isolated so production embeddings, pgvector, Pinecone, or an LLM API can be added without rewriting the API layer.

## Next Steps

- PostgreSQL + pgvector
- OpenAI/Anthropic model provider
- document chunking
- PDF ingestion
- JWT authentication
- async database access
- background ingestion jobs
- CI with GitHub Actions
- cloud deployment
