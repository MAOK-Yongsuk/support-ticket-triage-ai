"""Tool: Search past tickets for similar issues and their resolutions."""

import json
from pathlib import Path

# Load ticket history from JSON
_DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
with open(_DATA_DIR / "ticket_history.json", encoding="utf-8") as f:
    TICKET_HISTORY = json.load(f)


def search_ticket_history(customer_id: str = None, query: str = None) -> dict:
    """Search past tickets for similar issues and their resolutions.

    Use this tool to find how similar issues were resolved in the past.
    This helps provide consistent resolutions and learn from previous
    support interactions. Can search by customer ID, issue keywords, or both.

    Args:
        customer_id: Optional customer ID to filter by specific customer's history.
        query: Optional search query for issue type or keywords
               (e.g., "payment failure", "error 500", "dark mode").

    Returns:
        dict: A dictionary containing:
            - status: "success" or "no_results"
            - similar_tickets: List of past tickets with resolution info
            - common_resolution: Most frequent resolution method (if multiple found)
            - avg_resolution_time_hours: Average time to resolve similar issues
            - total_results: Number of matching tickets found
    """
    filtered_tickets = TICKET_HISTORY

    # Filter by customer ID if provided
    if customer_id:
        filtered_tickets = [
            t for t in filtered_tickets if t["customer_id"] == customer_id
        ]

    # Filter by query if provided
    if query:
        query_lower = query.lower()
        query_terms = query_lower.split()
        scored_tickets = []

        for ticket in filtered_tickets:
            score = 0
            searchable = (
                f"{ticket['subject']} {ticket['issue_type']} {ticket['product_area']}"
            ).lower()

            for term in query_terms:
                if term in searchable:
                    score += 1

            if score > 0:
                scored_tickets.append((score, ticket))

        scored_tickets.sort(key=lambda x: x[0], reverse=True)
        filtered_tickets = [t for _, t in scored_tickets]

    if filtered_tickets:
        # Calculate common resolution and avg time
        resolutions = [t["resolution"] for t in filtered_tickets]
        resolution_times = [t["resolution_time_hours"] for t in filtered_tickets]

        # Find most common resolution (simple frequency count)
        resolution_counts = {}
        for res in resolutions:
            resolution_counts[res] = resolution_counts.get(res, 0) + 1
        common_resolution = max(resolution_counts, key=resolution_counts.get)

        avg_time = sum(resolution_times) / len(resolution_times)

        return {
            "status": "success",
            "similar_tickets": [
                {
                    "ticket_id": t["ticket_id"],
                    "date": t["date"],
                    "subject": t["subject"],
                    "issue_type": t["issue_type"],
                    "resolution": t["resolution"],
                    "resolution_time_hours": t["resolution_time_hours"],
                    "satisfaction": t["satisfaction"],
                }
                for t in filtered_tickets[:5]  # Top 5 results
            ],
            "common_resolution": common_resolution,
            "avg_resolution_time_hours": round(avg_time, 1),
            "total_results": len(filtered_tickets),
        }

    return {
        "status": "no_results",
        "similar_tickets": [],
        "total_results": 0,
        "message": "No similar tickets found in history",
    }
