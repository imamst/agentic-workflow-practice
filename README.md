## Agentic MLBB Draft Research Workflow

This project is a **Python-based agentic workflow** for running deep research on **Mobile Legends: Bang Bang (MLBB) draft pick strategies**.  
It combines **FastAPI**, **Celery + Redis**, **OpenRouter-hosted LLMs**, and **Tavily** web search to:

- **Generate search queries** for a given MLBB draft strategy
- **Search the web** and summarize results with LLMs
- **Compose a structured strategy report** using a detailed system prompt
- **Export the report as a PDF** via HTML → PDF rendering

---

## Project Structure

- **`main.py`**: Simple script version of the research pipeline (no Celery/FastAPI).
- **`app/main.py`**: Scripted research runner that generates queries, searches the web, and writes `output.pdf`.
- **`app/fastapi-main.py`**: FastAPI application exposing a `/research` endpoint and a `/scalar` API reference UI.
- **`app/celery_app.py`**: Celery configuration (broker + backend using Redis) and task autodiscovery.
- **`app/modules/research/schema.py`**: Pydantic models for queries and API input payloads.
- **`app/modules/research/methods.py`**: Core agentic logic:
  - `generate_queries(topic: str)` – uses OpenRouter LLM to produce web search queries.
  - `search_web(query: str)` – uses Tavily to search and an LLM to summarize results.
  - `generate_report(strategy: str, research_context: str)` – uses an LLM and a rich system prompt to create the final report.
- **`app/modules/research/prompt.py`**: Long-form `REPORT_SYSTEM_PROMPT` describing report format and tone.
- **`app/modules/research/tasks.py`**: Celery task `research_task` that runs the research pipeline and writes `output.pdf`.
- **`app/utils/openai.py`**: OpenRouter `OpenAI` client configured via `OPENROUTER_API_KEY`.
- **`app/utils/tavily.py`**: Tavily client configured via `TAVILY_API_KEY`.

---

## Features

- **Agentic research pipeline**
  - Uses one LLM call to generate focused web search queries.
  - Uses Tavily to fetch rich web results.
  - Uses LLM reasoning to summarize and synthesize findings.
- **MLBB-specific strategy report**
  - Draft-phase focused (bans and picks).
  - Detailed, reproducible report structure defined in `REPORT_SYSTEM_PROMPT`.
- **Asynchronous task processing**
  - Celery + Redis worker for running potentially long research jobs.
- **API-first design**
  - FastAPI endpoint to trigger research asynchronously.
  - Scalar endpoint serving interactive API reference docs.
- **PDF export**
  - Converts Markdown report content to HTML and then to PDF using `weasyprint`.

---

## Requirements

Core technologies and services:

- **Python** (3.11+ recommended)
- **Redis** running locally on `redis://localhost:6379/0`
- **OpenRouter API key** (`OPENROUTER_API_KEY`)
- **Tavily API key** (`TAVILY_API_KEY`)

Python dependencies are defined in `pyproject.toml` / `uv.lock` and include, for example:

- `fastapi`
- `uvicorn`
- `celery`
- `redis`
- `pydantic`
- `python-dotenv`
- `weasyprint`
- `tavily-python` (or equivalent Tavily client)
- `openai` (for the OpenRouter-compatible client)
- `scalar-fastapi`

---

## Setup

1. **Clone the repository**

```bash
git clone <your-repo-url>.git
cd agentic-workflow
```

2. **Create and activate a virtual environment** (example with `venv`)

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. **Install dependencies**

If you are using `uv` (recommended with `pyproject.toml` + `uv.lock`):

```bash
uv sync
```

Or with `pip`:

```bash
pip install -e .
```

4. **Configure environment variables**

Create a `.env` file in the project root (same folder as `pyproject.toml`) and set:

```bash
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Ensure Redis is running locally on `redis://localhost:6379/0`, or adjust `broker`/`backend` URLs in `app/celery_app.py`.

---

## Running the Research Script (CLI)

You can run the script-based pipeline directly without the API:

```bash
python -m app.main
```

This will:

- Generate queries for the hardcoded topic `"Mobile Legends Bang Bang Draft Picks Strategy"`.
- Search the web and build up a research context.
- Generate a report for the `"Pick off"` draft strategy.
- Render the result to `output.pdf` in the project root.

---

## Running the API + Worker

### 1. Start Redis

Make sure Redis is running locally. On Windows, you can use WSL, Docker, or a native Redis port.

### 2. Start the Celery worker

From the project root:

```bash
celery -A app.celery_app.celery_app worker --loglevel=info
```

### 3. Start the FastAPI server

From the project root:

```bash
uvicorn app.fastapi-main:app --reload
```

This will start the FastAPI app on `http://127.0.0.1:8000`.

---

### Running via `Makefile` (with `uv`)

If you have `uv` installed and want a shorter workflow, you can use the provided `Makefile` targets:

- **Start the FastAPI dev server**

  ```bash
  make dev
  ```

- **Start the Celery worker**

  ```bash
  make celery
  ```

These targets internally call `uv run` with the appropriate commands defined in `Makefile`.

---

## API Usage

- **POST** ` /research`
  - **Body** (`application/json`):
    ```json
    {
      "strategy": "Pick off"
    }
    ```
  - **Behavior**: Enqueues a Celery job via `research_task.delay(strategy=...)`.  
    When the task completes, it writes `output.pdf` to the current working directory.

- **GET** `/scalar`
  - Returns a Scalar UI (API reference) based on the current FastAPI OpenAPI schema.

You can use any HTTP client (curl, Postman, Thunder Client, etc.) to call these endpoints.

---

## How the Agentic Workflow Works

1. **Query Generation**
   - `generate_queries(topic)` calls an LLM via OpenRouter to produce web search queries for the given topic.
2. **Web Search + Summarization**
   - For each query, `search_web(query)` calls Tavily for web results, then uses another LLM call to summarize those results into concise context.
3. **Report Generation**
   - All summarized snippets are concatenated into a `research_context`.
   - `generate_report(strategy, research_context)` uses a long, structured `REPORT_SYSTEM_PROMPT` to produce a comprehensive MLBB draft strategy report.
4. **PDF Rendering**
   - The report (Markdown) is converted to HTML and then to a PDF file `output.pdf` using `weasyprint`.
5. **Task Orchestration**
   - When using the API, `research_task` is executed asynchronously via Celery so the HTTP request returns quickly while the report generation runs in the background.

---

## Development Notes

- Adjust the **topic** and **strategy** in `app/main.py` or in your API request body to explore different MLBB draft strategies.
- If you change the report format, update `REPORT_SYSTEM_PROMPT` in `app/modules/research/prompt.py`.
- For production use, you should:
  - Externalize Redis configuration (URLs, passwords, TLS).
  - Add proper logging and error handling.
  - Persist generated PDFs and job metadata (e.g., in S3 or a database) instead of writing directly to the working directory.

---
