"""Tool: Look up recent billing transactions and their status."""

import json
from pathlib import Path

# Load billing transactions from JSON
_DATA_DIR = Path(__file__).parent.parent.parent / "data"
with open(_DATA_DIR / "billing_transactions.json", encoding="utf-8") as f:
    BILLING_TRANSACTIONS = json.load(f)


def lookup_billing_transaction(customer_id: str, amount: float = None) -> dict:
    """Look up recent billing transactions for a customer.

    Use this tool to investigate payment and billing issues. This helps
    identify duplicate charges, pending authorization holds, and transaction
    status without needing to escalate to the billing team immediately.

    Args:
        customer_id: The unique customer identifier (e.g., "CUST-001").
        amount: Optional transaction amount to filter by (e.g., 29.99).

    Returns:
        dict: A dictionary containing:
            - status: "found" or "not_found"
            - transactions: List of matching transactions with details
            - total_pending: Total amount in pending/authorization holds
            - total_completed: Total amount in completed transactions
            - total_results: Number of matching transactions
    """
    # Filter transactions by customer ID
    customer_txns = [
        t for t in BILLING_TRANSACTIONS if t["customer_id"] == customer_id
    ]

    # Further filter by amount if provided
    if amount is not None:
        customer_txns = [t for t in customer_txns if abs(t["amount"] - amount) < 0.01]

    if customer_txns:
        total_pending = sum(
            t["amount"] for t in customer_txns if t["status"] == "pending"
        )
        total_completed = sum(
            t["amount"] for t in customer_txns if t["status"] == "completed"
        )

        return {
            "status": "found",
            "transactions": [
                {
                    "transaction_id": t["transaction_id"],
                    "amount": t["amount"],
                    "currency": t["currency"],
                    "status": t["status"],
                    "type": t["type"],
                    "created_at": t["created_at"],
                    "card_last4": t["card_last4"],
                }
                for t in customer_txns
            ],
            "total_pending": round(total_pending, 2),
            "total_completed": round(total_completed, 2),
            "total_results": len(customer_txns),
        }

    return {
        "status": "not_found",
        "transactions": [],
        "total_results": 0,
        "message": f"No billing transactions found for customer ID: '{customer_id}'",
    }
