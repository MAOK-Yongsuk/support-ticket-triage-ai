"""Tool: Check SLA status and time remaining before breach."""

import json
from pathlib import Path

# Load SLA status from JSON
_DATA_DIR = Path(__file__).parent.parent.parent / "data"
with open(_DATA_DIR / "sla_status.json", encoding="utf-8") as f:
    SLA_STATUS = json.load(f)


def check_sla_status(customer_id: str) -> dict:
    """Check if customer has active SLA and time remaining before breach.

    Use this tool to determine if a ticket is approaching its SLA deadline.
    This helps prioritize tickets that are at risk of SLA breach, especially
    for enterprise customers with strict response time requirements.

    Args:
        customer_id: The unique customer identifier (e.g., "CUST-001").

    Returns:
        dict: A dictionary containing:
            - status: "found" or "not_found"
            - sla_tier: SLA level (e.g., "enterprise_4h", "pro_24h", "free_72h")
            - response_time_hours: Total hours allowed for first response
            - time_remaining_hours: Hours remaining until SLA breach
            - is_at_risk: True if less than 25% of time remaining
            - ticket_opened_at: ISO timestamp when ticket was opened
    """
    sla = SLA_STATUS.get(customer_id)

    if sla:
        return {
            "status": "found",
            "sla_tier": sla["sla_tier"],
            "response_time_hours": sla["response_time_hours"],
            "time_remaining_hours": sla["time_remaining_hours"],
            "is_at_risk": sla["is_at_risk"],
            "ticket_opened_at": sla["ticket_opened_at"],
        }

    return {
        "status": "not_found",
        "message": f"No SLA information found for customer ID: '{customer_id}'",
    }
