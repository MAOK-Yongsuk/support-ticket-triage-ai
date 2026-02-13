"""Tool: Check current queue depth and wait time for specialist teams."""

import json
from pathlib import Path

# Load agent availability from JSON
_DATA_DIR = Path(__file__).parent.parent.parent / "data"
with open(_DATA_DIR / "agent_availability.json", encoding="utf-8") as f:
    AGENT_AVAILABILITY = json.load(f)


def get_agent_availability(team: str = None) -> dict:
    """Check current queue depth and wait time for a specialist team.

    Use this tool to make informed routing decisions. Route tickets to
    teams with shorter wait times, or escalate immediately if all teams
    are overwhelmed. This helps balance load and improve response times.

    Args:
        team: Optional team name to check (e.g., "billing_team", "infra_team", "product_team").
              If not provided, returns availability for all teams.

    Returns:
        dict: A dictionary containing:
            - status: "found" or "not_found"
            - team_name: Name of the team
            - current_queue_depth: Number of tickets in queue
            - avg_wait_time_minutes: Average wait time for next available agent
            - agents_available: Number of agents currently available
            - agents_total: Total number of agents on the team
    """
    if team:
        team_data = AGENT_AVAILABILITY.get(team)
        if team_data:
            return {
                "status": "found",
                "team_name": team_data["team_name"],
                "current_queue_depth": team_data["current_queue_depth"],
                "avg_wait_time_minutes": team_data["avg_wait_time_minutes"],
                "agents_available": team_data["agents_available"],
                "agents_total": team_data["agents_total"],
            }
        else:
            return {
                "status": "not_found",
                "message": f"No availability information for team: '{team}'",
            }

    # Return all teams if no specific team requested
    return {
        "status": "found",
        "teams": AGENT_AVAILABILITY,
    }
