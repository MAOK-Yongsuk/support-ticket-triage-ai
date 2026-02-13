"""CLI runner — processes all sample tickets through the triage agent."""

import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from triage_agent.agent import root_agent
from triage_agent.sample_tickets import SAMPLE_TICKETS

load_dotenv()

async def process_ticket(
    runner: Runner,
    session_service: InMemorySessionService,
    ticket: dict,
) -> str:
    """Send a single ticket to the triage agent and return the response."""

    # Build user message
    conversation = "\n\n".join(
        f"[{msg['timestamp']}] {msg['content']}" for msg in ticket["messages"]
    )
    user_message = (
        f"Please triage the following support ticket.\n\n"
        f"**Ticket ID:** {ticket['ticket_id']}\n"
        f"**Customer ID:** {ticket['customer_id']}\n"
        f"**Subject:** {ticket['subject']}\n\n"
        f"**Messages:**\n{conversation}"
    )

    # Create session and run
    session = await session_service.create_session(
        app_name="support_triage",
        user_id=ticket["customer_id"],
    )

    agent_response = ""
    async for event in runner.run_async(
        session_id=session.id,
        user_id=ticket["customer_id"],
        new_message=types.Content(
            role="user",
            parts=[types.Part(text=user_message)],
        ),
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                agent_response = event.content.parts[0].text
            else:
                 agent_response = "No response content."


    return agent_response


async def main():
    """Process all sample tickets and print results."""

    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="support_triage",
        session_service=session_service,
    )

    print("=" * 80)
    print("  SUPPORT TICKET TRIAGE AGENT — Processing Sample Tickets")
    print("=" * 80)

    for i, ticket in enumerate(SAMPLE_TICKETS, 1):
        print(f"\n{'─' * 80}")
        print(f"  Ticket {i}/{len(SAMPLE_TICKETS)}: {ticket['ticket_id']}")
        print(f"  Subject: {ticket['subject']}")
        print(f"  Customer: {ticket['customer_id']}")
        print(f"{'─' * 80}\n")

        response = await process_ticket(runner, session_service, ticket)

        print(response)
        print()

    print("=" * 80)
    print("  All tickets processed.")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
