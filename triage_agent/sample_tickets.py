"""Sample support tickets from the homework assignment."""

SAMPLE_TICKETS: list[dict] = [
    # --- Ticket 1: Payment failure with escalating frustration ---
    {
        "ticket_id": "TK-2026-0101",
        "customer_id": "CUST-001",
        "subject": "Payment failed during Pro upgrade - multiple charges",
        "messages": [
            {
                "timestamp": "3 hours ago",
                "content": (
                    "My payment failed when I tried to upgrade to Pro. "
                    "Can you check what's wrong?"
                ),
            },
            {
                "timestamp": "2 hours ago",
                "content": (
                    "I tried again with a different card. Now I see TWO "
                    "pending charges but my account still shows Free plan??"
                ),
            },
            {
                "timestamp": "1 hour ago",
                "content": (
                    "Okay this is getting ridiculous. Just checked my bank app "
                    "- I have THREE charges of $29.99 now. None of them refunded. "
                    "And I STILL don't have Pro access."
                ),
            },
            {
                "timestamp": "just now",
                "content": (
                    "HELLO?? Is anyone there??? I need this fixed NOW. I have "
                    "a presentation in 2 hours and I need the Pro export features. "
                    "If these charges aren't reversed by end of day I'm disputing "
                    "all of them with my bank."
                ),
            },
        ],
    },
    # --- Ticket 2: Enterprise outage in Thailand (Thai language) ---
    {
        "ticket_id": "TK-2026-0102",
        "customer_id": "CUST-002",
        "subject": "System down - Error 500 - Enterprise - Thailand region",
        "messages": [
            {
                "timestamp": "2 hours ago",
                "content": (
                    "ระบบเข้าไม่ได้ครับ ขึ้น error 500\n"
                    "(Translation: Can't access the system, showing error 500)"
                ),
            },
            {
                "timestamp": "1.5 hours ago",
                "content": (
                    "ลองหลายเครื่องแล้ว ทั้ง Chrome, Safari, Firefox ผลเหมือนกันหมด "
                    "เพื่อนร่วมงานก็เข้าไม่ได้เหมือนกัน\n"
                    "(Translation: Tried multiple machines - Chrome, Safari, Firefox "
                    "- same result. Coworkers also can't access)"
                ),
            },
            {
                "timestamp": "45 mins ago",
                "content": (
                    "ตอนนี้ลูกค้าโวยเข้ามาเยอะมาก เรามี demo กับลูกค้ารายใหญ่บ่ายนี้ "
                    "ถ้าระบบไม่กลับมา deal นี้อาจจะหลุด\n"
                    "(Translation: Customers are flooding in with complaints now. "
                    "We have a demo with a major client this afternoon. If the "
                    "system doesn't come back, we might lose this deal)"
                ),
            },
            {
                "timestamp": "just now",
                "content": (
                    "เช็ค status.company.com แล้ว บอกว่า all systems operational "
                    "แต่เราใช้งานไม่ได้จริงๆ ช่วยเช็คให้หน่อยได้ไหมครับ "
                    "region Asia มีปัญหาหรือเปล่า?\n"
                    "(Translation: Checked status.company.com - it says all systems "
                    "operational, but we really can't use it. Can you please check? "
                    "Is there an issue with the Asia region?)"
                ),
            },
        ],
    },
    # --- Ticket 3: Friendly feature question about dark mode ---
    {
        "ticket_id": "TK-2026-0103",
        "customer_id": "CUST-003",
        "subject": "Dark mode question and feature request",
        "messages": [
            {
                "timestamp": "2 days ago",
                "content": (
                    "Hey, just wondering if you support dark mode? No rush 😊"
                ),
            },
            {
                "timestamp": "1 day ago",
                "content": (
                    "Thanks for the reply! Oh nice, so it's in Settings > Appearance. "
                    "Found it! But hmm I'm on Pro plan and I only see 'Light' and "
                    "'System Default' options. No dark mode toggle?"
                ),
            },
            {
                "timestamp": "1 day ago (3 hours later)",
                "content": (
                    "Okay so I switched to 'System Default' and my Mac is set to "
                    "dark mode, but your app still shows light theme. Is this a "
                    "bug or am I missing something?"
                ),
            },
            {
                "timestamp": "today",
                "content": (
                    "Also random question while I have you - is there a way to "
                    "schedule dark mode? Like auto-switch at 6pm? Some apps have "
                    "that. Would be cool if you guys added it 👀"
                ),
            },
        ],
    },
]
