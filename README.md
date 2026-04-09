# RAG Customer Support Agent

## Overview
A Retrieval-Augmented Generation (RAG) powered Customer Support Agent that can answer customer queries by retrieving relevant information from a documentation/knowledge base.

## Features (Planned)
- Document indexing & vector database integration.
- LLM-based response generation.
- Support for multiple document formats (PDF, DOCX, Markdown).
- API integration for customer support platforms.

## Project Structure
- `data/`: Knowledge base documents.
- `src/`: Backend logic and RAG implementation.
- `notebooks/`: Experimentation and prototyping.
- `docs/`: Design documents and project planning.

## How to use

1. **Setup Environment**:
   ```bash
   cp .env.example .env
   # Add your Google API key to .env
   ```

2. **Ingest Data**:
   Place your PDF or Markdown documents in the `data/` directory.
   ```bash
   python src/ingest.py
   ```

3. **Run the API Server**:
   ```bash
   python src/api.py
   # Or using uvicorn directly:
   # uvicorn src.api:app --reload
   ```

4. **Query the API**:
   You can interact with the agent via the `/api/ask` endpoint:
   ```bash
   curl -X POST "http://localhost:8000/api/ask" \
        -H "Content-Type: application/json" \
        -d '{"question":"What is your return policy?"}'
   ```
   
   The OpenAPI documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).
