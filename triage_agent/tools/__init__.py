"""Tool functions for the triage agent."""

from triage_agent.tools.agent_availability import get_agent_availability
from triage_agent.tools.billing_lookup import lookup_billing_transaction
from triage_agent.tools.customer_history import lookup_customer_history
from triage_agent.tools.health_score import get_customer_health_score
from triage_agent.tools.knowledge_base import search_knowledge_base
from triage_agent.tools.sla_status import check_sla_status
from triage_agent.tools.system_status import check_system_status
from triage_agent.tools.ticket_history import search_ticket_history

__all__ = [
    # Core tools (original)
    "search_knowledge_base",
    "lookup_customer_history",
    # High-priority tools
    "check_sla_status",
    "search_ticket_history",
    "get_customer_health_score",
    # Nice-to-have tools
    "check_system_status",
    "lookup_billing_transaction",
    "get_agent_availability",
]
