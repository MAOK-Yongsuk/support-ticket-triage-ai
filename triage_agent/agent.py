"""Support Ticket Triage Agent — ADK agent definition."""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from triage_agent.prompts import TRIAGE_AGENT_INSTRUCTION
from triage_agent.tools import search_knowledge_base, lookup_customer_history


root_agent = LlmAgent(
    model=LiteLlm(model="openai/gpt-4o"),
    name="support_triage_agent",
    description=(
        "An AI agent that triages incoming customer support tickets by "
        "classifying urgency, extracting key information, searching a "
        "knowledge base, and deciding the appropriate next action."
    ),
    instruction=TRIAGE_AGENT_INSTRUCTION,
    tools=[search_knowledge_base, lookup_customer_history],
)
