"""Tool functions for the triage agent."""

from triage_agent.tools.knowledge_base import search_knowledge_base
from triage_agent.tools.customer_history import lookup_customer_history

__all__ = ["search_knowledge_base", "lookup_customer_history"]
