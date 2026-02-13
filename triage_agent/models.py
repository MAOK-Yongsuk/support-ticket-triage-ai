"""Pydantic models for structured triage output."""

from pydantic import BaseModel, Field


class ExtractedInfo(BaseModel):
    """Key information extracted from the support ticket."""

    product_area: str = Field(
        description="Product area affected (e.g., 'billing', 'platform', 'ui', 'api')"
    )
    issue_type: str = Field(
        description="Type of issue (e.g., 'payment_failure', 'outage', 'bug', 'feature_request')"
    )
    customer_sentiment: str = Field(
        description="Overall customer sentiment (e.g., 'frustrated', 'angry', 'neutral', 'positive')"
    )
    language: str = Field(
        description="Primary language of the messages (e.g., 'english', 'thai')"
    )


class RecommendedAction(BaseModel):
    """Recommended triage action."""

    action: str = Field(
        description="One of: 'auto_respond', 'route_to_specialist', 'escalate_to_human'"
    )
    route_to: str | None = Field(
        default=None,
        description="Target team if routing to specialist (e.g., 'billing_team', 'infra_team')",
    )
    reason: str = Field(
        description="Brief explanation of why this action was chosen"
    )


class TriageResult(BaseModel):
    """Complete triage analysis result for a support ticket."""

    urgency: str = Field(
        description="Urgency level: 'critical', 'high', 'medium', or 'low'"
    )
    extracted_info: ExtractedInfo
    recommended_action: RecommendedAction
    reasoning: str = Field(
        description="Detailed explanation of the triage decision"
    )
    draft_response: str = Field(
        description="Draft response to send to the customer"
    )
