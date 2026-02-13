"""Support Ticket Triage Agent — ADK agent definition."""

import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from triage_agent.prompts import TRIAGE_AGENT_INSTRUCTION
from triage_agent.tools import (
    check_sla_status,
    check_system_status,
    get_agent_availability,
    get_customer_health_score,
    lookup_billing_transaction,
    lookup_customer_history,
    search_knowledge_base,
    search_ticket_history,
)

# Load configuration from environment
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))

root_agent = LlmAgent(
    model=LiteLlm(
        model=f"openai/{MODEL_NAME}",
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    ),
    name="support_triage_agent",
    description=(
        "An AI agent that triages incoming customer support tickets by "
        "classifying urgency, extracting key information, searching a "
        "knowledge base, and deciding the appropriate next action."
    ),
    instruction=TRIAGE_AGENT_INSTRUCTION,
    tools=[
        # Context Tools
        lookup_customer_history,
        search_ticket_history,
        get_customer_health_score,

        # Knowledge Tools
        search_knowledge_base,

        # Operational Tools
        check_system_status,
        lookup_billing_transaction,
        check_sla_status,

        # Routing Tools
        get_agent_availability,
    ],
)