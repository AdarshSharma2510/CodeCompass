# CodeCompass

CodeCompass is an AI-powered repository Q&A assistant. A user uploads a GitHub repository as a ZIP file, and the system indexes the code so the user can ask natural-language questions about the repository. The assistant retrieves relevant code context, reranks results, and generates grounded answers using a local Ollama model.

The project has two parts:

* **Backend**: the main technical component, built with FastAPI, LangChain, ChromaDB, FlashRank, and Ollama.
* **Frontend**: a clean React/Vite interface that lets the user upload a repository and chat with it.

The backend is already working. The frontend is a simple, polished chat interface that connects to the backend API.

---

## What CodeCompass Does

1. The user uploads a repository ZIP file.
2. The backend extracts the repository.
3. The backend scans useful source files and documentation.
4. The files are loaded into LangChain documents.
5. The documents are chunked.
6. Embeddings are generated with a Hugging Face sentence-transformer model.
7. The chunks are stored in ChromaDB.
8. When the user asks a question, ChromaDB retrieves relevant chunks.
9. FlashRank reranks the retrieved chunks.
10. The selected context is sent to a local Ollama LLM.
11. The LLM returns a grounded answer based on the repository context.
12. The frontend displays the response in a Markdown chat UI.

The system is designed to answer questions such as:

* Where is the authentication implemented?
* How is the user interface structured?
* What does the main application entry point do?
* Where is a specific function or feature defined?

If the repository does not contain the answer, the assistant should say it cannot find the information in the retrieved repository context instead of inventing a file or behavior.

---

## Project Scope

This MVP intentionally supports:

* One active repository at a time
* One active chat session at a time
* Repository replacement by uploading a new ZIP
* Local backend execution
* Local Ollama LLM execution
* No authentication
* No multi-user support
* No multi-repository management
* Desktop-first usage

---

## Tech Stack

### Backend

* FastAPI
* Uvicorn
* LangChain
* ChromaDB
* FlashRank
* Hugging Face sentence-transformers
* Ollama
* Pydantic Settings

### Frontend

* React
* Vite
* Tailwind CSS
* `react-markdown`
* `remark-gfm`
* `rehype-highlight`
* `lucide-react`

---

## Backend Architecture

The backend follows a modular pipeline:

```text
Repository ZIP
    ↓
Extract
    ↓
Scan files
    ↓
Load documents
    ↓
Split into chunks
    ↓
Generate embeddings
    ↓
Store in ChromaDB
    ↓
Retrieve candidates
    ↓
Rerank with FlashRank
    ↓
Send context + chat history to Ollama
    ↓
Return grounded answer
```

### Backend responsibilities

* Repository extraction
* File scanning
* Document loading
* Chunking
* Embedding generation
* Vector storage
* Retrieval
* Reranking
* LLM response generation
* Chat history/session behavior

---

## Frontend Architecture

The frontend is intentionally simple and polished. It provides:

* ZIP repository upload
* Repository indexing status
* Chat UI for asking questions
* Markdown rendering for answers
* Syntax highlighting for code blocks
* Scrollable conversation area
* Fixed input area at the bottom
* End chat button
* Reset behavior when a new repository is uploaded

The frontend is designed to make it obvious that the user is chatting with a repository-aware coding assistant, not a generic chatbot.

---

## Current Frontend Behavior

The frontend supports the full basic flow:

1. Select a repository ZIP file.
2. Upload it to the backend.
3. Wait while the repository is indexed.
4. Show repository indexing status.
5. Ask questions about the repository.
6. Display user questions and assistant answers in chat bubbles.
7. Render assistant responses as Markdown.
8. Render code blocks with syntax highlighting.
9. Keep the conversation area scrollable.
10. Keep the input visible at the bottom of the screen.
11. Allow the user to upload a different repository.
12. Reset the frontend chat messages when a new repository is uploaded.

The application currently supports one active repository only.

---

## Backend API

### `GET /health`

Returns a simple health check response.

Example:

```json
{
  "status": "healthy"
}
```

### `POST /repositories/upload`

Uploads a repository ZIP file.

Expected form-data field:

* `file`

Example successful response:

```json
{
  "message": "Repository indexed successfully."
}
```

Important behavior:

* Uploading a new repository clears the current chat session.
* The repository is indexed into ChromaDB.
* The backend is designed for one active repository at a time.

### `POST /chat`

Sends a question to the repository assistant.

Example request:

```json
{
  "question": "Where is the Kanban board implemented?"
}
```

Example response:

```json
{
  "answer": "..."
}
```

Special behavior:

* If the user types `End`, the chat session is cleared and the backend returns a session-ended response.

---

## Chat Session Behavior

The project uses a simple single-session chat memory model.

The active chat history is stored in a file-based session. The session:

* is reused for follow-up questions,
* is cleared when a new repository is uploaded,
* is cleared when the user types `End`.

This keeps the project simple while still allowing multi-turn chat behavior.

---

## Repository Ingestion Flow

The ingestion pipeline works as follows:

1. The repository ZIP is uploaded through the API.
2. The ZIP is saved temporarily.
3. The repository is extracted.
4. Files are scanned.
5. Relevant files are loaded into LangChain documents.
6. Documents are chunked.
7. Chunks are embedded.
8. The embedded chunks are stored in ChromaDB.
9. The temporary upload file is removed.

The repository content that matters for retrieval is stored in the vector database, not as the original ZIP file.

---

## Retrieval and Reranking

The retrieval pipeline is:

1. Embed the user question.
2. Retrieve a larger set of candidate chunks from ChromaDB.
3. Rerank the candidates with FlashRank.
4. Keep the best chunks.
5. Send those chunks to the LLM.

This improves answer quality and reduces irrelevant retrieval results.

---

## LLM Behavior

The assistant uses a local Ollama model.

The LLM is instructed to:

* answer only from the retrieved repository context and chat history,
* avoid inventing files or behavior,
* say when the repository context does not contain the answer,
* mention file paths only when they are explicitly present in the retrieved context.

This grounding is important because the assistant should behave like a codebase-aware helper, not a general-purpose guessing model.

---

## Repository Content Handling

The backend scans and indexes useful source files and documentation files.

Temporary, generated, and unnecessary files are ignored, such as:

* `.venv`
* `__pycache__`
* `node_modules`
* build artifacts
* generated local data
* temporary upload files

The project is intentionally built around one repository at a time.

---

## File Structure

### Backend

```text
backend/
├── app/
│   ├── api/
│   │   ├── health.py
│   │   ├── repository.py
│   │   └── chat.py
│   ├── chat/
│   │   └── memory.py
│   ├── config/
│   │   ├── logging.py
│   │   └── settings.py
│   ├── ingestion/
│   │   ├── extractor.py
│   │   ├── loader.py
│   │   ├── pipeline.py
│   │   ├── scanner.py
│   │   └── splitter.py
│   ├── llm/
│   │   ├── model.py
│   │   ├── prompts.py
│   │   └── service.py
│   ├── retrieval/
│   │   └── retriever.py
│   ├── vectorstore/
│   │   ├── chroma.py
│   │   ├── embeddings.py
│   │   └── indexer.py
│   └── main.py
├── data/
│   ├── chat/
│   ├── chroma/
│   ├── repository/
│   └── uploads/
└── tests/
```

### Frontend

```text
frontend/
├── public/
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── index.html
├── package.json
├── package-lock.json
└── vite.config.js
```

---

## Environment Variables

The backend reads configuration from `.env`.

Important variables include:

```env
APP_NAME=CodeCompass
APP_VERSION=1.0.0
HF_ACCESS_TOKEN=your_huggingface_token_here
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

The backend also uses project-local paths for generated data such as ChromaDB and repository extraction.

Do not commit `.env` to Git.

---

## Local Setup

### Backend

Install backend dependencies, then run the API with Uvicorn.

Typical backend development server:

```text
http://127.0.0.1:8000
```

### Frontend

Install frontend dependencies, then run the Vite dev server.

Typical frontend development server:

```text
http://localhost:5173
```

The frontend uses the backend API base URL:

```javascript
const API_BASE_URL = "http://127.0.0.1:8000";
```

---

## CORS

During development, the frontend and backend run on different local origins:

* `http://localhost:5173`
* `http://127.0.0.1:8000`

The backend was updated to allow the frontend origin so the upload and chat requests work correctly in the browser.

---

## Current Status

The MVP is functional.

The full flow works:

```text
Upload Repository ZIP
    ↓
Backend Extracts Repository
    ↓
Backend Scans Files
    ↓
Backend Creates Documents
    ↓
Backend Chunks Documents
    ↓
Backend Generates Embeddings
    ↓
Backend Stores Vectors
    ↓
Frontend Shows Repository Ready
    ↓
User Asks Question
    ↓
Backend Retrieves Relevant Context
    ↓
Backend Reranks Context
    ↓
Ollama Generates Answer
    ↓
Frontend Displays Grounded Answer
```

The backend is the main technical highlight of the project. The frontend is intentionally polished but not overly complex.

---

## Notes on Ignored Files

A root-level `.gitignore` is used to prevent generated, local, and sensitive files from being committed.

Important ignored items include:

```text
__pycache__/
.venv/
venv/
.env
.env.*
node_modules/
dist/
build/
.vite/
data/
chroma_db/
chroma/
*.sqlite
*.sqlite3
.cache/
huggingface/
hf_cache/
*.log
.vscode/
.idea/
.pytest_cache/
.mypy_cache/
.ruff_cache/
```

A safe `.env.example` file may be committed if needed.

---

## Summary

CodeCompass is an AI repository assistant that turns a repository ZIP into a conversational knowledge base.

The backend performs the AI/RAG pipeline:

* ingestion,
* chunking,
* embeddings,
* vector search,
* reranking,
* local LLM response generation.

The frontend provides the user experience:

* upload a repository,
* ask questions,
* read grounded answers,
* reset the session when needed.

The system is intentionally simple in product scope, but the backend is a strong example of a codebase-aware RAG assistant built with FastAPI, LangChain, ChromaDB, FlashRank, and Ollama.
