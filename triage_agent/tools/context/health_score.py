"""Tool: Get customer health score and churn risk assessment."""

import json
from pathlib import Path

# Load health metrics from JSON
_DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
with open(_DATA_DIR / "health_metrics.json", encoding="utf-8") as f:
    HEALTH_METRICS = json.load(f)


def get_customer_health_score(customer_id: str) -> dict:
    """Calculate customer churn risk based on usage, satisfaction, and engagement.

    Use this tool to assess if a customer is at risk of churning. This helps
    prioritize tickets from at-risk customers to prevent churn and maintain
    customer satisfaction.

    Args:
        customer_id: The unique customer identifier (e.g., "CUST-001").

    Returns:
        dict: A dictionary containing:
            - status: "found" or "not_found"
            - health_score: 0-100 score (lower = higher churn risk)
            - risk_level: "high" (0-50), "medium" (51-75), or "low" (76-100)
            - recent_nps: Net Promoter Score from last survey (0-10)
            - usage_trend: "increasing", "stable", or "declining"
            - last_login_days_ago: Days since last login
            - feature_adoption_pct: Percentage of available features used
    """
    metrics = HEALTH_METRICS.get(customer_id)

    if metrics:
        return {
            "status": "found",
            "health_score": metrics["health_score"],
            "risk_level": metrics["risk_level"],
            "recent_nps": metrics["recent_nps"],
            "usage_trend": metrics["usage_trend"],
            "last_login_days_ago": metrics["last_login_days_ago"],
            "feature_adoption_pct": metrics["feature_adoption_pct"],
        }

    return {
        "status": "not_found",
        "message": f"No health metrics found for customer ID: '{customer_id}'",
    }
