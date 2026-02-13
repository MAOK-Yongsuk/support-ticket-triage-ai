# Support Ticket Triage Agent

An AI agent that triages incoming customer support tickets — built with **Google ADK**, **FastAPI**, and **OpenAI GPT-4o** (via LiteLLM).

## What It Does

### Phase 1: Core Triage
1. **Classifies urgency** — critical / high / medium / low
2. **Extracts key info** — product area, issue type, sentiment, language
3. **Searches a knowledge base** — finds relevant FAQ/docs articles
4. **Checks customer history** — plan tier, tenure, past tickets

### Phase 2: Advanced Context (New)
5. **Checks SLA status** — time remaining before breach (Enterprise/Pro)
6. **Searches ticket history** — finds similar past issues and resolutions
7. **Calculates health score** — churn risk, usage trends, NPS
8. **Checks system status** — detects active regional outages
9. **Looks up billing** — validates transaction status and authorization holds
10. **Checks agent availability** — routes to teams with shortest queues

### Phase 3: Decision
11. **Decides next action** — auto-respond, route to specialist (with team load balancing), or escalate to human

## Project Structure

```
├── triage_agent/               # ADK agent package
│   ├── agent.py                # Root agent definition (8 tools wired)
│   ├── prompts.py              # System prompt
│   ├── models.py               # Pydantic response models
│   ├── sample_tickets.py       # 3 sample tickets
│   └── tools/                  # Tool definitions
│       ├── knowledge_base.py   # Search KB tool
│       ├── customer_history.py # Customer lookup tool
│       ├── sla_status.py       # SLA checker
│       ├── ticket_history.py   # Similarity search
│       ├── health_score.py     # Churn risk calculator
│       ├── system_status.py    # Incident checker
│       ├── billing_lookup.py   # Transaction finder
│       └── agent_availability.py # Queue depth checker
├── data/                       # Mock datasets (JSON)
│   ├── knowledge_base.json     # 9 FAQ/doc articles
│   ├── customers.json          # Customer records
│   ├── ticket_history.json     # Historical tickets
│   ├── health_metrics.json     # Churn risk data
│   ├── sla_status.json         # Active SLA timers
│   ├── system_status.json      # Regional incidents
│   ├── billing_transactions.json # Payment logs
│   └── agent_availability.json # Team queue stats
├── tests/                      # Unit tests
│   ├── test_knowledge_base.py  # KB search tool tests
│   └── test_customer_history.py# Customer lookup tests
├── eval/                       # Agent evaluation
│   ├── golden_dataset.py       # Labeled test cases
│   └── eval_runner.py          # Accuracy measurement
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

### Run Tests

```bash
uv run pytest tests/ -v
```

### Run Agent Evaluation (requires `OPENAI_API_KEY`)

```bash
python -m eval.eval_runner
```

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
