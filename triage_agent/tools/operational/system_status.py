"""Tool: Check for ongoing incidents or maintenance in a region."""

import json
from pathlib import Path

# Load system status from JSON
_DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
with open(_DATA_DIR / "system_status.json", encoding="utf-8") as f:
    SYSTEM_STATUS = json.load(f)


def check_system_status(region: str = None) -> dict:
    """Check for ongoing incidents or maintenance affecting service availability.

    Use this tool to determine if a customer's issue is related to a known
    system outage or incident. This helps avoid escalating tickets for
    issues that are already being addressed by the infrastructure team.

    Args:
        region: Optional region to check (e.g., "US", "EU", "Thailand").
                If not provided, returns global status and all regions.

    Returns:
        dict: A dictionary containing:
            - global_status: Overall system status ("operational", "degraded", "outage")
            - region_status: Status for the specified region (if provided)
            - incidents: List of active incidents affecting the region
            - last_updated: ISO timestamp of last status update
    """
    global_status = SYSTEM_STATUS["global"]["status"]
    last_updated = SYSTEM_STATUS["global"]["last_updated"]

    if region:
        region_data = SYSTEM_STATUS["regions"].get(region)
        if region_data:
            return {
                "global_status": global_status,
                "region": region,
                "region_status": region_data["status"],
                "incidents": region_data["incidents"],
                "last_updated": last_updated,
            }
        else:
            return {
                "global_status": global_status,
                "region": region,
                "region_status": "unknown",
                "incidents": [],
                "last_updated": last_updated,
                "message": f"No status information for region: '{region}'",
            }

    # Return all regions if no specific region requested
    return {
        "global_status": global_status,
        "regions": SYSTEM_STATUS["regions"],
        "last_updated": last_updated,
    }
