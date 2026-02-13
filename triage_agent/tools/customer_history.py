"""Tool: Look up customer history and profile information."""

from data.customers import CUSTOMER_RECORDS


def lookup_customer_history(customer_id: str) -> dict:
    """Look up a customer's profile, plan details, and support ticket history.

    Use this tool to understand the customer's context: their plan tier,
    how long they've been a customer, their spending, and any previous
    support interactions. This helps inform urgency classification and
    the appropriate triage action.

    Args:
        customer_id: The unique customer identifier (e.g., "CUST-001").

    Returns:
        dict: A dictionary containing:
            - status: "found" or "not_found"
            - customer: Customer profile with plan, region, tenure, spend,
                        previous tickets, and notes (when found)
    """
    customer = CUSTOMER_RECORDS.get(customer_id)

    if customer:
        return {
            "status": "found",
            "customer": {
                "customer_id": customer["customer_id"],
                "name": customer["name"],
                "plan": customer["plan"],
                "region": customer["region"],
                "tenure_months": customer["tenure_months"],
                "seats": customer["seats"],
                "monthly_spend": customer["monthly_spend"],
                "previous_tickets": customer["previous_tickets"],
                "total_previous_tickets": len(customer["previous_tickets"]),
                "notes": customer["notes"],
            },
        }

    return {
        "status": "not_found",
        "message": f"No customer record found for ID: '{customer_id}'",
    }
