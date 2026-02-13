"""Golden dataset for evaluating the triage agent's classification accuracy.

Each entry contains a sample ticket and the expected triage output.
Use this with eval_runner.py to measure agent performance.
"""

GOLDEN_DATASET: list[dict] = [
    # --- Ticket 1: Payment failure → expected HIGH urgency ---
    {
        "ticket_id": "EVAL-001",
        "customer_id": "CUST-001",
        "subject": "Payment failed during Pro upgrade - multiple charges",
        "messages": [
            {"timestamp": "3 hours ago", "content": "My payment failed when I tried to upgrade to Pro. Can you check what's wrong?"},
            {"timestamp": "2 hours ago", "content": "I tried again with a different card. Now I see TWO pending charges but my account still shows Free plan??"},
            {"timestamp": "1 hour ago", "content": "Okay this is getting ridiculous. Just checked my bank app - I have THREE charges of $29.99 now. None of them refunded. And I STILL don't have Pro access."},
            {"timestamp": "just now", "content": "HELLO?? Is anyone there??? I need this fixed NOW. I have a presentation in 2 hours and I need the Pro export features. If these charges aren't reversed by end of day I'm disputing all of them with my bank."},
        ],
        "expected": {
            "urgency": "high",
            "product_area": "billing",
            "issue_type": "payment_failure",
            "sentiment": "angry",
            "action": "escalate_to_human",
        },
    },
    # --- Ticket 2: Enterprise outage → expected CRITICAL urgency ---
    {
        "ticket_id": "EVAL-002",
        "customer_id": "CUST-002",
        "subject": "System down - Error 500 - Enterprise - Thailand region",
        "messages": [
            {"timestamp": "2 hours ago", "content": "ระบบเข้าไม่ได้ครับ ขึ้น error 500 (Can't access the system, showing error 500)"},
            {"timestamp": "1.5 hours ago", "content": "ลองหลายเครื่องแล้ว ทั้ง Chrome, Safari, Firefox ผลเหมือนกันหมด เพื่อนร่วมงานก็เข้าไม่ได้เหมือนกัน (Tried multiple machines - same result. Coworkers also can't access)"},
            {"timestamp": "45 mins ago", "content": "ตอนนี้ลูกค้าโวยเข้ามาเยอะมาก เรามี demo กับลูกค้ารายใหญ่บ่ายนี้ ถ้าระบบไม่กลับมา deal นี้อาจจะหลุด (Customers flooding in with complaints. We have a demo this afternoon. Might lose the deal)"},
            {"timestamp": "just now", "content": "เช็ค status.company.com แล้ว บอกว่า all systems operational แต่เราใช้งานไม่ได้จริงๆ region Asia มีปัญหาหรือเปล่า? (Status page says all operational but we really can't use it. Asia region issue?)"},
        ],
        "expected": {
            "urgency": "critical",
            "product_area": "platform",
            "issue_type": "outage",
            "sentiment": "frustrated",
            "action": "escalate_to_human",
        },
    },
    # --- Ticket 3: Dark mode question → expected LOW urgency ---
    {
        "ticket_id": "EVAL-003",
        "customer_id": "CUST-003",
        "subject": "Dark mode question and feature request",
        "messages": [
            {"timestamp": "2 days ago", "content": "Hey, just wondering if you support dark mode? No rush 😊"},
            {"timestamp": "1 day ago", "content": "Thanks for the reply! Oh nice, so it's in Settings > Appearance. Found it! But hmm I'm on Pro plan and I only see 'Light' and 'System Default' options. No dark mode toggle?"},
            {"timestamp": "1 day ago", "content": "Okay so I switched to 'System Default' and my Mac is set to dark mode, but your app still shows light theme. Is this a bug or am I missing something?"},
            {"timestamp": "today", "content": "Also random question while I have you - is there a way to schedule dark mode? Like auto-switch at 6pm? Some apps have that. Would be cool if you guys added it 👀"},
        ],
        "expected": {
            "urgency": "low",
            "product_area": "ui",
            "issue_type": "bug",
            "sentiment": "positive",
            "action": "auto_respond",
        },
    },
    # --- Ticket 4: API Rate Limit (Pro Customer) → expected MEDIUM urgency ---
    {
        "ticket_id": "EVAL-004",
        "customer_id": "CUST-003",
        "subject": "API 429 Too Many Requests",
        "messages": [
            {"timestamp": "1 hour ago", "content": "Hi, we're suddenly getting 429 errors on all our API calls. We're on the Pro plan which should have 1000 req/day. We've only made about 200 calls today."},
            {"timestamp": "30 mins ago", "content": "This is blocking our internal dashboard sync. Can you check if there's a limit issue?"},
        ],
        "expected": {
            "urgency": "medium",
            "product_area": "api",
            "issue_type": "bug",
            "sentiment": "neutral",
            "action": "route_to_specialist",
        },
    },
    # --- Ticket 5: Enterprise SLA Inquiry → expected LOW urgency ---
    {
        "ticket_id": "EVAL-005",
        "customer_id": "CUST-002",
        "subject": "Question about our SLA terms",
        "messages": [
            {"timestamp": "yesterday", "content": "To whom it may concern, could you clarify our current SLA response times for critical incidents? We are updating our internal vendor docs."},
        ],
        "expected": {
            "urgency": "low",
            "product_area": "other",
            "issue_type": "question",
            "sentiment": "neutral",
            "action": "auto_respond",
        },
    },
    # --- Ticket 6: Login Issue (SSO) → expected HIGH urgency ---
    {
        "ticket_id": "EVAL-006",
        "customer_id": "CUST-002",
        "subject": "SSO Login Failure - Multiple Users",
        "messages": [
            {"timestamp": "10 mins ago", "content": "All our marketing team members are unable to log in via Okta SSO. We're getting an 'Invalid Certificate' error."},
            {"timestamp": "5 mins ago", "content": "This is affecting about 15 users right now."},
        ],
        "expected": {
            "urgency": "high",
            "product_area": "authentication",
            "issue_type": "bug",
            "sentiment": "neutral",
            "action": "escalate_to_human",
        },
    },
    # --- Ticket 7: Refund Request (Friendly) → expected MEDIUM urgency ---
    {
        "ticket_id": "EVAL-007",
        "customer_id": "CUST-001",
        "subject": "Charged twice by mistake?",
        "messages": [
            {"timestamp": "1 day ago", "content": "Hi there! I think I accidentally clicked the upgrade button twice. I see two charges on my card for this month. Could you please refund one of them? Thanks!"},
        ],
        "expected": {
            "urgency": "medium",
            "product_area": "billing",
            "issue_type": "payment_failure",
            "sentiment": "positive",
            "action": "route_to_specialist",
        },
    },
    # --- Ticket 8: Feature Request (Mobile App) → expected LOW urgency ---
    {
        "ticket_id": "EVAL-008",
        "customer_id": "CUST-003",
        "subject": "Mobile App??",
        "messages": [
            {"timestamp": "2 days ago", "content": "Love the web version! Do you guys have an iOS app coming soon? Would be super helpful for checking stats on the go."},
        ],
        "expected": {
            "urgency": "low",
            "product_area": "platform",
            "issue_type": "feature_request",
            "sentiment": "positive",
            "action": "auto_respond",
        },
    },
]
