"""FastAPI server for the Support Ticket Triage Agent."""

import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel, Field

from triage_agent.agent import root_agent

load_dotenv()

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Support Ticket Triage Agent",
    description="AI-powered triage for customer support tickets",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# ADK runner (shared across requests)
# ---------------------------------------------------------------------------
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="support_triage",
    session_service=session_service,
)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class TicketMessage(BaseModel):
    """A single message within a support ticket."""

    timestamp: str = Field(description="When the message was sent")
    content: str = Field(description="Message content")


class TicketRequest(BaseModel):
    """Incoming support ticket for triage."""

    ticket_id: str = Field(description="Unique ticket identifier")
    customer_id: str = Field(description="Customer identifier")
    subject: str = Field(description="Ticket subject line")
    messages: list[TicketMessage] = Field(description="Conversation messages")


class TriageResponse(BaseModel):
    """Triage result returned by the agent."""

    ticket_id: str
    agent_response: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "agent": root_agent.name}


@app.post("/triage", response_model=TriageResponse)
async def triage_ticket(ticket: TicketRequest):
    """Process a support ticket through the triage agent.

    Sends the ticket to the ADK agent, which will:
    1. Look up customer history
    2. Search the knowledge base
    3. Classify urgency and extract key info
    4. Recommend a triage action
    """
    # Build the user message from the ticket
    conversation = "\n\n".join(
        f"[{msg.timestamp}] {msg.content}" for msg in ticket.messages
    )
    user_message = (
        f"Please triage the following support ticket.\n\n"
        f"**Ticket ID:** {ticket.ticket_id}\n"
        f"**Customer ID:** {ticket.customer_id}\n"
        f"**Subject:** {ticket.subject}\n\n"
        f"**Messages:**\n{conversation}"
    )

    # Create a session and run the agent
    session = await session_service.create_session(
        app_name="support_triage",
        user_id=ticket.customer_id,
    )

    try:
        agent_response_text = ""
        async for event in runner.run_async(
            session_id=session.id,
            user_id=ticket.customer_id,
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=user_message)],
            ),
        ):
            # Collect the final agent response
            if event.is_final_response() and event.content and event.content.parts:
                agent_response_text = event.content.parts[0].text

        if not agent_response_text:
            raise HTTPException(
                status_code=500,
                detail="Agent did not produce a response",
            )

        return TriageResponse(
            ticket_id=ticket.ticket_id,
            agent_response=agent_response_text,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent processing failed: {str(e)}",
        )
