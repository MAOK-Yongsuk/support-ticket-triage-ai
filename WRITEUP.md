# Write-Up: Support Ticket Triage Agent

## Architecture Decisions

**Google ADK + LiteLLM for OpenAI GPT-4o**
I chose Google ADK as the agent framework because it provides a clean, opinionated structure for building AI agents with tool-calling capabilities. Since the assignment requires OpenAI GPT, I integrated it via ADK's official LiteLLM connector — this keeps the framework benefits (runner, sessions, tool schema auto-generation) while using GPT-4o as the underlying model.

**FastAPI as the API Layer**
FastAPI provides automatic OpenAPI documentation, request validation (via Pydantic), and async support — ideal for wrapping an async ADK agent. The API is intentionally minimal (`POST /triage` + `GET /health`) to stay focused on the core triage logic.

**Separation of Concerns**
The codebase is split into clear layers:
- `triage_agent/` — agent definition, prompt, and tools (pure AI logic)
- `data/` — JSON datasets (Customers, History, etc.) + TXT files for Knowledge Base
- `app.py` / `main.py` — presentation layer (API and CLI)

This separation means you can swap the data layer to use a real database, change the model, or add new tools without touching the core agent logic.

**Tool Design**
**Tool Design (8 Tools)**
Tools are plain Python functions with detailed docstrings. We expanded from 2 to 8 tools to provide comprehensive context:
1.  **Core:** `search_knowledge_base`, `lookup_customer_history`
2.  **High-Priority:** `check_sla_status`, `search_ticket_history`, `get_customer_health_score`
3.  **Operational:** `check_system_status`, `lookup_billing_transaction`, `get_agent_availability`

Each tool loads data from a dedicated JSON file in `data/`, simulating real database/API responses. The knowledge base search uses keyword scoring with tag boosting.

## What Could Go Wrong

| Risk | Impact | Mitigation |
|------|--------|------------|
| **LLM hallucination** | Agent invents customer data or KB articles | Tools return real data; prompt instructs agent to rely on tool outputs, not assumptions |
| **Token limit exceeded** | Long ticket threads could exceed context window | Truncate/summarize older messages before sending; monitor token usage |
| **Tool call failures** | Agent skips tools or calls with wrong parameters | System prompt explicitly requires both tool calls; validate tool outputs before using |
| **Non-English input** | LLM may misinterpret non-English text | GPT-4o handles multilingual well; prompt instructs to note detected language |
| **Prompt injection** | Malicious ticket content manipulates the agent | Separate system prompt from user content; input sanitization in production |
| **Latency** | Multiple tool calls + LLM round-trips add latency | Cache frequent KB queries; use async processing; consider streaming responses |

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
- A/B test prompt variations to optimize accuracy
- Expand the knowledge base based on common escalation topics
- Add new tools as needed (e.g., SLA checker, billing system integration)
