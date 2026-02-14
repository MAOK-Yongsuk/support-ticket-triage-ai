"""Evaluation runner — measures triage agent accuracy against golden dataset.

Usage:
    python -m eval.eval_runner

Requires OPENAI_API_KEY in .env
"""

import asyncio
import json
import re
from collections import Counter, defaultdict

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


def calculate_f1(true_pos, false_pos, false_neg):
    """Calculate Precision, Recall, and F1 score."""
    precision = true_pos / (true_pos + false_pos) if (true_pos + false_pos) > 0 else 0
    recall = true_pos / (true_pos + false_neg) if (true_pos + false_neg) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1


def print_metrics_report(results: list[dict]):
    """Print a detailed classification report."""
    
    urgency_classes = ["critical", "high", "medium", "low"]
    
    # Initialize counters
    tp = Counter() # True Positives
    fp = Counter() # False Positives
    fn = Counter() # False Negatives
    confusion = defaultdict(Counter) # confusion[actual][predicted]

    # Metrics for other fields
    field_correct = Counter()
    total_count = len(results)

    for r in results:
        # Urgency Metrics
        actual_urg = r["expected"]["urgency"]
        pred_urg = r["parsed"].get("urgency", "unknown").lower()
        
        confusion[actual_urg][pred_urg] += 1
        
        if actual_urg == pred_urg:
            tp[actual_urg] += 1
            field_correct["urgency"] += 1
        else:
            fp[pred_urg] += 1
            fn[actual_urg] += 1

        # Other Fields Metrics
        for field in ["product_area", "issue_type", "sentiment", "action", "language"]:
            if r["checks"].get(field):
                field_correct[field] += 1

    print("\n" + "="*60)
    print("  DETAILED METRICS REPORT")
    print("="*60)

    # 1. Overall Accuracy per Category
    print("\n--- Category Accuracy ---")
    for field in ["urgency", "product_area", "issue_type", "sentiment", "action", "language"]:
        acc = (field_correct[field] / total_count * 100) if total_count > 0 else 0
        print(f"{field.ljust(15)}: {acc:.1f}%")

    # 2. Urgency Classification Metrics (Precision/Recall/F1)
    print("\n--- Urgency Classification Metrics ---")
    print(f"{'Class':<12} {'Precision':<10} {'Recall':<10} {'F1-Score':<10} {'Support':<8}")
    print("-" * 55)

    macro_f1_sum = 0
    macro_count = 0

    for cls in urgency_classes:
        true_p = tp[cls]
        false_p = fp[cls]
        false_n = fn[cls]
        support = true_p + false_n # Total actual instances
        
        prec, rec, f1 = calculate_f1(true_p, false_p, false_n)
        
        if support > 0:
            macro_f1_sum += f1
            macro_count += 1
            
        print(f"{cls:<12} {prec:.2f}      {rec:.2f}      {f1:.2f}      {support:<8}")

    macro_f1 = macro_f1_sum / macro_count if macro_count > 0 else 0
    print("-" * 55)
    print(f"Macro Avg F1: {macro_f1:.2f}")

    # 3. Confusion Matrix
    print("\n--- Confusion Matrix (Actual ↓ vs Predicted →) ---")
    print(f"{'':<10} {'crit':<6} {'high':<6} {'med':<6} {'low':<6}")
    for actual in urgency_classes:
        row_str = f"{actual:<10}"
        for pred in urgency_classes:
            count = confusion[actual][pred]
            row_str += f" {count:<6}"
        print(row_str)
    print("="*60 + "\n")


def evaluate_result(parsed: dict, expected: dict) -> dict:
    """Compare parsed agent output against expected values."""
    checks = {}

    # Urgency match
    checks["urgency"] = parsed.get("urgency", "").lower() == expected["urgency"]

    extracted = parsed.get("extracted_info", {})
    
    # Product area
    checks["product_area"] = extracted.get("product_area", "").lower() == expected["product_area"]

    # Issue type (flexible)
    agent_issue = extracted.get("issue_type", "").lower()
    checks["issue_type"] = expected["issue_type"] in agent_issue or agent_issue in expected["issue_type"]

    # Sentiment (flexible)
    agent_sentiment = extracted.get("customer_sentiment", "").lower()
    sentiment_groups = [
        {"angry", "frustrated", "upset", "furious", "negative"},
        {"positive", "friendly", "happy", "satisfied"},
        {"neutral", "calm", "anxious"}, # Anxious can bridge neutral/negative depending on context
    ]
    expected_sentiment = expected["sentiment"]
    checks["sentiment"] = agent_sentiment == expected_sentiment or any(
        agent_sentiment in group and expected_sentiment in group
        for group in sentiment_groups
    )

    # Language (new field)
    expected_lang = expected.get("language", "english") # Default to english if not specified
    agent_lang = extracted.get("language", "english").lower()
    checks["language"] = agent_lang == expected_lang

    # Action match
    action = parsed.get("recommended_action", {})
    checks["action"] = action.get("action", "").lower() == expected["action"]

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
    print("  TRIAGE AGENT EVALUATION (ENHANCED)")
    print("=" * 80)

    all_results = []

    for entry in GOLDEN_DATASET:
        ticket_id = entry["ticket_id"]
        print(f"\nEvaluating: {ticket_id}...")

        # Build user message (Prompt construction)
        conversation = "\n".join(
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
        try:
            async for event in runner.run_async(
                session_id=session.id,
                user_id=entry["customer_id"],
                new_message=types.Content(role="user", parts=[types.Part(text=user_message)]),
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    agent_response = event.content.parts[0].text
        except Exception as e:
            print(f"❌ Error running agent: {e}")
            continue

        # Parse and evaluate
        parsed = extract_json_from_response(agent_response)
        
        result_entry = {
            "ticket_id": ticket_id,
            "expected": entry["expected"],
            "parsed": parsed if parsed else {},
            "raw_response": agent_response,
            "checks": {}
        }

        if parsed:
            checks = evaluate_result(parsed, entry["expected"])
            result_entry["checks"] = checks
            
            # Print quick status
            status_icons = [
                "✅" if checks.get(k) else f"❌({k})" 
                for k in ["urgency", "action", "language"]
            ]
            print(f"  Result: {' '.join(status_icons)}")
        else:
            print("  ⚠️  Parse Error")

        all_results.append(result_entry)

    # Print Full Report
    print_metrics_report(all_results)


if __name__ == "__main__":
    asyncio.run(run_evaluation())
