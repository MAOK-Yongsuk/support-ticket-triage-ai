"""Evaluation runner — measures triage agent accuracy against golden dataset.

Usage:
    python -m eval.eval_runner

Requires OPENAI_API_KEY in .env
"""

import asyncio
import json
import re

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from eval.golden_dataset import GOLDEN_DATASET
from triage_agent.agent import root_agent

load_dotenv()


def extract_json_from_response(text: str) -> dict | None:
    """Attempt to extract JSON from the agent's response text."""
    # Try to find JSON block in markdown code fences
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to parse the entire text as JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    return None


def evaluate_result(parsed: dict, expected: dict) -> dict:
    """Compare parsed agent output against expected values.

    Returns a dict with per-field match results and an overall score.
    """
    checks = {}

    # Urgency match
    agent_urgency = parsed.get("urgency", "").lower()
    checks["urgency"] = agent_urgency == expected["urgency"]

    # Product area match
    extracted = parsed.get("extracted_info", {})
    agent_area = extracted.get("product_area", "").lower()
    checks["product_area"] = agent_area == expected["product_area"]

    # Issue type match (flexible — allow partial match)
    agent_issue = extracted.get("issue_type", "").lower()
    checks["issue_type"] = expected["issue_type"] in agent_issue or agent_issue in expected["issue_type"]

    # Sentiment match (flexible — allow similar sentiments)
    agent_sentiment = extracted.get("customer_sentiment", "").lower()
    sentiment_groups = [
        {"angry", "frustrated", "upset", "furious"},
        {"positive", "friendly", "happy", "satisfied"},
        {"neutral", "calm"},
    ]
    expected_sentiment = expected["sentiment"]
    checks["sentiment"] = agent_sentiment == expected_sentiment or any(
        agent_sentiment in group and expected_sentiment in group
        for group in sentiment_groups
    )

    # Action match
    action = parsed.get("recommended_action", {})
    agent_action = action.get("action", "").lower()
    checks["action"] = agent_action == expected["action"]

    # Overall score
    total = len(checks)
    passed = sum(1 for v in checks.values() if v)
    checks["score"] = f"{passed}/{total}"
    checks["score_pct"] = round(passed / total * 100) if total > 0 else 0

    return checks


async def run_evaluation():
    """Run the agent on all golden dataset entries and report accuracy."""

    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="triage_eval",
        session_service=session_service,
    )

    print("=" * 80)
    print("  TRIAGE AGENT EVALUATION")
    print("=" * 80)

    all_results = []

    for entry in GOLDEN_DATASET:
        ticket_id = entry["ticket_id"]
        print(f"\n{'─' * 80}")
        print(f"  Evaluating: {ticket_id} — {entry['subject']}")
        print(f"{'─' * 80}")

        # Build user message
        conversation = "\n\n".join(
            f"[{msg['timestamp']}] {msg['content']}" for msg in entry["messages"]
        )
        user_message = (
            f"Please triage the following support ticket.\n\n"
            f"**Ticket ID:** {entry['ticket_id']}\n"
            f"**Customer ID:** {entry['customer_id']}\n"
            f"**Subject:** {entry['subject']}\n\n"
            f"**Messages:**\n{conversation}"
        )

        # Run agent
        session = await session_service.create_session(
            app_name="triage_eval",
            user_id=entry["customer_id"],
        )

        agent_response = ""
        async for event in runner.run_async(
            session_id=session.id,
            user_id=entry["customer_id"],
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=user_message)],
            ),
        ):
            if event.is_final_response() and event.content and event.content.parts:
                agent_response = event.content.parts[0].text

        # Parse and evaluate
        parsed = extract_json_from_response(agent_response)
        if parsed:
            result = evaluate_result(parsed, entry["expected"])
            all_results.append(result)
            print(f"  Score: {result['score']} ({result['score_pct']}%)")
            for field, match in result.items():
                if field not in ("score", "score_pct"):
                    status = "✅" if match else "❌"
                    print(f"    {status} {field}")
        else:
            print("  ⚠️  Could not parse JSON from agent response")
            print(f"  Raw response:\n{agent_response[:500]}")
            all_results.append({"score_pct": 0})

    # Summary
    print(f"\n{'=' * 80}")
    print("  EVALUATION SUMMARY")
    print(f"{'=' * 80}")
    avg_score = sum(r["score_pct"] for r in all_results) / len(all_results) if all_results else 0
    print(f"  Tickets evaluated: {len(all_results)}")
    print(f"  Average accuracy:  {avg_score:.0f}%")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    asyncio.run(run_evaluation())
