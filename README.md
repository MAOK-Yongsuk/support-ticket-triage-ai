# Support Ticket Triage Agent

An AI agent that triages incoming customer support tickets — built with **Google ADK**, **FastAPI**, and **OpenAI GPT-4o** (via LiteLLM).

## What It Does

1. **Classifies urgency** — critical / high / medium / low
2. **Extracts key info** — product area, issue type, sentiment, language
3. **Searches a knowledge base** — finds relevant FAQ/docs articles
4. **Checks customer history** — plan tier, tenure, past tickets
5. **Decides next action** — auto-respond, route to specialist, or escalate to human

## Project Structure

```
├── triage_agent/               # ADK agent package
│   ├── agent.py                # Root agent definition
│   ├── prompts.py              # System prompt
│   ├── models.py               # Pydantic response models
│   ├── sample_tickets.py       # 3 sample tickets
│   └── tools/                  # Tool definitions
│       ├── knowledge_base.py   # Search KB tool
│       └── customer_history.py # Customer lookup tool
├── data/                       # Mock datasets
│   ├── knowledge_base.py       # 9 FAQ/doc articles
│   └── customers.py            # 3 customer records
├── app.py                      # FastAPI server
├── main.py                     # CLI runner
└── pyproject.toml              # Dependencies
```

## Setup

### 1. Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### 2. Install Dependencies

```bash
# With uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-key-here
```

## Running

### Option A: CLI Runner (Process Sample Tickets)

```bash
python main.py
```

This processes the 3 sample tickets from the assignment and prints triage results.

### Option B: FastAPI Server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Then send a POST request:

```bash
curl -X POST http://localhost:8000/triage \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TK-001",
    "customer_id": "CUST-001",
    "subject": "Payment issue",
    "messages": [
      {"timestamp": "now", "content": "My payment failed during upgrade"}
    ]
  }'
```

### Option C: ADK Dev UI

```bash
adk web
```

Open http://localhost:8000, select `triage_agent`, and chat with the agent directly.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/triage` | Process a support ticket |

## Tech Stack

- **[Google ADK](https://google.github.io/adk-docs/)** — Agent Development Kit
- **[LiteLLM](https://docs.litellm.ai/)** — OpenAI GPT-4o integration
- **[FastAPI](https://fastapi.tiangolo.com/)** — API framework
- **[Pydantic](https://docs.pydantic.dev/)** — Data validation
