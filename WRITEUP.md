# Write-Up: Support Ticket Triage Agent

## Architecture Decisions

**Google ADK + LiteLLM for OpenAI GPT-4o**
I chose Google ADK as the agent framework because it provides a clean, opinionated structure for building AI agents with tool-calling capabilities. Since the assignment requires OpenAI GPT, I integrated it via ADK's official LiteLLM connector — this keeps the framework benefits (runner, sessions, tool schema auto-generation) while using GPT-4o as the underlying model.

**FastAPI as the API Layer**
FastAPI provides automatic OpenAPI documentation, request validation (via Pydantic), and async support — ideal for wrapping an async ADK agent. The API is intentionally minimal (`POST /triage` + `GET /health`) to stay focused on the core triage logic.

**Separation of Concerns & Modular Design**
The codebase is split into clear layers:
- `triage_agent/` — agent definition, prompt, and tools (pure AI logic)
  - `tools/` — Reorganized into logical subdirectories: `context`, `search`, `operational`, `routing`
- `data/` — JSON datasets (Customers, History, etc.) + TXT files for Knowledge Base
- `app.py` / `main.py` — presentation layer (API and CLI)

This separation means you can swap the data layer to use a real database, change the model, or add new tools without touching the core agent logic.

**Tool Design (8 Tools)**
Tools are plain Python functions with detailed docstrings, now organized by domain:
1.  **Context:** `lookup_customer_history`, `search_ticket_history`, `get_customer_health_score`, `check_sla_status`
2.  **Search (RAG):** `search_knowledge_base` using ChromaDB + OpenAI Embeddings
3.  **Operational:** `check_system_status`, `lookup_billing_transaction`
4.  **Routing:** `get_agent_availability`

We migrated the Knowledge Base from a simple JSON file to a **RAG (Retrieval-Augmented Generation)** system using ChromaDB. This allows for semantic search ("payment failed" finds "Billing Issues"), significantly improving relevance over the previous keyword-based approach. Other tools load data from dedicated JSON files in `data/`, simulating real database/API responses.

## What Could Go Wrong

| Risk | Impact | Mitigation |
|------|--------|------------|
| **LLM hallucination** | Agent invents customer data or KB articles | Tools return real data; prompt instructs agent to rely on tool outputs, not assumptions |
| **Semantic Drift** | RAG retrieves irrelevant articles | Tune chunking strategy and embedding model; fallback to keyword search (implemented) |
| **Token limit exceeded** | Long ticket threads/KB articles could exceed context | Truncate/summarize older messages; retrieved KB articles are top-k only |
| **Tool call failures** | Agent skips tools or calls with wrong parameters | System prompt requires tool calls; Pydantic validation catches schema errors |
| **Dependency Risks** | External services (OpenAI, ChromaDB) downtime | Implement retries and fallbacks (e.g., keyword search if vector DB fails) |

## How I'd Evaluate This Agent in Production

**Automated Metrics:**
- **Classification accuracy** — Build a golden dataset of labeled tickets; measure precision/recall per urgency level
- **Tool usage rate** — Track whether the agent calls both tools on every ticket (should be ~100%)
- **Response time** — P50/P95 latency from ticket submission to triage result
- **Action distribution** — Monitor the balance of auto-respond vs. escalate over time

**Human-in-the-Loop:**
- **QA sampling** — Human reviewers grade a random 10% of triage decisions on accuracy and appropriateness
- **Escalation feedback** — Track how often human agents override the AI triage decision; use disagreements to improve the prompt
- **Customer satisfaction** — For auto-responded tickets, measure CSAT and resolution rate

**Continuous Improvement:**
- **LLM-as-a-Judge:** Use a stronger model (e.g., GPT-5) to evaluate the triage decisions of smaller/faster models on complexity, empathy, and correctness.
- **A/B Testing:** comparison of prompt variations or RAG retrieval strategies (k=3 vs k=5).
- **Feedback Loop:** Automatically flag tickets where the human agent's resolution differed significantly from the AI's triage.

**Production Monitoring & Optimization:**
- **Continuous Evaluation:** Instead of a one-time test, evaluate agent logs in real-time or daily batches to identify when accuracy drifts.
- **Performance Tracking:** Compare current agent versions against baselines (e.g., previous versions) to ensure updates do not cause regression.
- **Live Alerts:** Set up monitoring for high latency (slow responses) or high error rates in tool calls, triggering automated alerts to the engineering team.
- **Adversarial Testing:** Intentionally putting the agent into challenging, edge-case scenarios to test its robustness against prompt injection or confusing inputs.