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
            {
                "timestamp": "3 hours ago",
                "content": "My payment failed when I tried to upgrade to Pro. Can you check what's wrong?",
            },
            {
                "timestamp": "2 hours ago",
                "content": "I tried again with a different card. Now I see TWO pending charges but my account still shows Free plan??",
            },
            {
                "timestamp": "1 hour ago",
                "content": "Okay this is getting ridiculous. Just checked my bank app - I have THREE charges of $29.99 now. None of them refunded. And I STILL don't have Pro access.",
            },
            {
                "timestamp": "just now",
                "content": "HELLO?? Is anyone there??? I need this fixed NOW. I have a presentation in 2 hours and I need the Pro export features. If these charges aren't reversed by end of day I'm disputing all of them with my bank.",
            },
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
            {
                "timestamp": "2 hours ago",
                "content": "ระบบเข้าไม่ได้ครับ ขึ้น error 500 (Can't access the system, showing error 500)",
            },
            {
                "timestamp": "1.5 hours ago",
                "content": "ลองหลายเครื่องแล้ว ทั้ง Chrome, Safari, Firefox ผลเหมือนกันหมด เพื่อนร่วมงานก็เข้าไม่ได้เหมือนกัน (Tried multiple machines - same result. Coworkers also can't access)",
            },
            {
                "timestamp": "45 mins ago",
                "content": "ตอนนี้ลูกค้าโวยเข้ามาเยอะมาก เรามี demo กับลูกค้ารายใหญ่บ่ายนี้ ถ้าระบบไม่กลับมา deal นี้อาจจะหลุด (Customers flooding in with complaints. We have a demo this afternoon. Might lose the deal)",
            },
            {
                "timestamp": "just now",
                "content": "เช็ค status.company.com แล้ว บอกว่า all systems operational แต่เราใช้งานไม่ได้จริงๆ region Asia มีปัญหาหรือเปล่า? (Status page says all operational but we really can't use it. Asia region issue?)",
            },
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
            {
                "timestamp": "2 days ago",
                "content": "Hey, just wondering if you support dark mode? No rush 😊",
            },
            {
                "timestamp": "1 day ago",
                "content": "Thanks for the reply! Oh nice, so it's in Settings > Appearance. Found it! But hmm I'm on Pro plan and I only see 'Light' and 'System Default' options. No dark mode toggle?",
            },
            {
                "timestamp": "1 day ago",
                "content": "Okay so I switched to 'System Default' and my Mac is set to dark mode, but your app still shows light theme. Is this a bug or am I missing something?",
            },
            {
                "timestamp": "today",
                "content": "Also random question while I have you - is there a way to schedule dark mode? Like auto-switch at 6pm? Some apps have that. Would be cool if you guys added it 👀",
            },
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
            {
                "timestamp": "1 hour ago",
                "content": "Hi, we're suddenly getting 429 errors on all our API calls. We're on the Pro plan which should have 1000 req/day. We've only made about 200 calls today.",
            },
            {
                "timestamp": "30 mins ago",
                "content": "This is blocking our internal dashboard sync. Can you check if there's a limit issue?",
            },
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
            {
                "timestamp": "yesterday",
                "content": "To whom it may concern, could you clarify our current SLA response times for critical incidents? We are updating our internal vendor docs.",
            },
        ],
        "expected": {
            "urgency": "low",
            "product_area": "other",
            "issue_type": "question",
            "sentiment": "neutral",
            "action": "auto_respond",
        },
    },
    # --- Ticket 6: Mixed Language (Thai/English) → expected HIGH urgency ---
    {
        "ticket_id": "EVAL-009",
        "customer_id": "CUST-004",
        "subject": "Login issues / เข้าสู่ระบบไม่ได้",
        "messages": [
            {
                "timestamp": "10 mins ago",
                "content": "Hello, I cannot login to my account.",
            },
            {
                "timestamp": "5 mins ago",
                "content": "พอกด login แล้วมันหมุนติ้วๆ ไม่ไปไหนเลยครับ (It keeps spinning when I click login).",
            },
            {
                "timestamp": "2 mins ago",
                "content": "Please help urgent! ต้องรีบใช้ดึง report ครับ (Need to pull report urgently).",
            },
        ],
        "expected": {
            "urgency": "high",
            "product_area": "authentication",
            "issue_type": "bug",
            "sentiment": "frustrated",
            "action": "escalate_to_human",
            "language": "thai",
        },
    },
    # --- Ticket 7: Ambiguous Urgency (High/Medium) → expected HIGH urgency ---
    # Scenario: Pro user, significant bug but workaround exists, but deadline approaching.
    {
        "ticket_id": "EVAL-010",
        "customer_id": "CUST-005",
        "subject": "Export function crashing large files",
        "messages": [
            {
                "timestamp": "2 hours ago",
                "content": "When I try to export 50k+ rows, the system crashes.",
            },
            {
                "timestamp": "1 hour ago",
                "content": "I can export in batches of 10k, but it's very manual and slow.",
            },
            {
                "timestamp": "30 mins ago",
                "content": "please fix this, I have a board meeting tomorrow morning and need the full dataset.",
            },
        ],
        "expected": {
            "urgency": "high",
            "product_area": "platform",
            "issue_type": "bug",
            "sentiment": "frustrated",
            "action": "route_to_specialist",  # Or escalate if wait time is high
        },
    },
    # --- Ticket 8: Security Flag (Potential Incident) → expected CRITICAL urgency ---
    {
        "ticket_id": "EVAL-008",
        "customer_id": "CUST-006",
        "subject": "Suspicious login alert",
        "messages": [
            {
                "timestamp": "15 mins ago",
                "content": "I just got an email saying a new device logged in from Russia. I am in California. I did not authorize this.",
            },
            {
                "timestamp": "10 mins ago",
                "content": "I see changes in my admin settings that I didn't make!",
            },
        ],
        "expected": {
            "urgency": "critical",
            "product_area": "security",
            "issue_type": "security_incident",
            "sentiment": "frustrated",
            "action": "escalate_to_human",
        },
    },
    # --- Ticket 9: Refund Request (Low Priority) ---
    {
        "ticket_id": "EVAL-009",
        "customer_id": "CUST-007",
        "subject": "Refund for unused month",
        "messages": [
            {
                "timestamp": "yesterday",
                "content": "Hi, I forgot to cancel my subscription last month. I haven't used the tool at all.",
            },
            {
                "timestamp": "today",
                "content": "Can I get a refund for the last charge? usage logs will show 0 activity.",
            },
        ],
        "expected": {
            "urgency": "low",
            "product_area": "billing",
            "issue_type": "refund_request",
            "sentiment": "neutral",
            "action": "route_to_specialist",  # Billing specialist
        },
    },
    # --- Ticket 10: Integration Error (Technical) ---
    {
        "ticket_id": "EVAL-010",
        "customer_id": "CUST-008",
        "subject": "Zapier integration failing",
        "messages": [
            {
                "timestamp": "2 hours ago",
                "content": "The Zapier webhook is returning 400 Bad Request since this morning.",
            },
            {
                "timestamp": "1 hour ago",
                "content": "Payload seems correct. Did you change the schema?",
            },
        ],
        "expected": {
            "urgency": "medium",
            "product_area": "api",
            "issue_type": "bug",
            "sentiment": "frustrated",
            "action": "route_to_specialist",  # Technical support
        },
    },
    # --- Ticket 11: GDPR Deletion Request (Legal) ---
    {
        "ticket_id": "EVAL-011",
        "customer_id": "CUST-009",
        "subject": "Data deletion request (GDPR)",
        "messages": [
            {
                "timestamp": "today",
                "content": "Please delete all my personal data in accordance with GDPR Article 17.",
            },
            {"timestamp": "today", "content": "Confirm via email when done."},
        ],
        "expected": {
            "urgency": "medium",
            "product_area": "other",
            "issue_type": "legal",
            "sentiment": "neutral",
            "action": "escalate_to_human",  # Legal/Compliance team
        },
    },
    # --- Ticket 12: Password Reset (Common) ---
    {
        "ticket_id": "EVAL-012",
        "customer_id": "CUST-010",
        "subject": "Forgot password link not working",
        "messages": [
            {
                "timestamp": "10 mins ago",
                "content": "I clicked 'forgot password' but never got the email.",
            },
            {"timestamp": "5 mins ago", "content": "Checked spam folder too. Nothing."},
        ],
        "expected": {
            "urgency": "medium",
            "product_area": "authentication",
            "issue_type": "bug",  # or access_issue
            "sentiment": "frustrated",  # mildly
            "action": "auto_respond",  # KB likely has "check spam" or "allowlist domain"
        },
    },
    # --- Ticket 13: Pure Thai - Data import issue → expected HIGH urgency ---
    {
        "ticket_id": "EVAL-013",
        "customer_id": "CUST-011",
        "subject": "นำเข้าข้อมูล Excel ไม่ได้ครับ",
        "messages": [
            {
                "timestamp": "3 hours ago",
                "content": "พยายามนำเข้าไฟล์ Excel ขนาด 20MB แต่ขึ้น error ว่า 'File too large'",
            },
            {
                "timestamp": "2 hours ago",
                "content": "ไฟล์ของลูกค้าเยอะมาก ต้อง import วันนี้เลยครับ งานหลุดแน่ๆ",
            },
            {
                "timestamp": "1 hour ago",
                "content": "ช่วยดูให้หน่อยครับ ใช้ Enterprise plan แล้วนะ",
            },
        ],
        "expected": {
            "urgency": "high",
            "product_area": "platform",
            "issue_type": "bug",
            "sentiment": "worried",
            "action": "escalate_to_human",
            "language": "thai",
        },
    },
    # --- Ticket 14: Feature request (enthusiastic) → expected LOW urgency ---
    {
        "ticket_id": "EVAL-014",
        "customer_id": "CUST-012",
        "subject": "LOVE the new features! Just one suggestion...",
        "messages": [
            {
                "timestamp": "yesterday",
                "content": "Hey team! Absolutely loving the new dashboard redesign! 🎉 The dark mode is amazing and the speed is so much better!",
            },
            {
                "timestamp": "yesterday",
                "content": "One tiny suggestion - would be super cool if we could customize the widget colors. Would match our company branding better!",
            },
            {
                "timestamp": "today",
                "content": "No rush at all! Just sharing some feedback. Keep up the awesome work! 💪",
            },
        ],
        "expected": {
            "urgency": "low",
            "product_area": "ui",
            "issue_type": "feature_request",
            "sentiment": "positive",
            "action": "auto_respond",
        },
    },
    # --- Ticket 15: Performance issue → expected MEDIUM urgency ---
    {
        "ticket_id": "EVAL-015",
        "customer_id": "CUST-013",
        "subject": "Dashboard loading very slow",
        "messages": [
            {
                "timestamp": "4 hours ago",
                "content": "Dashboard is taking 30+ seconds to load today. Usually it's under 5 seconds.",
            },
            {
                "timestamp": "3 hours ago",
                "content": "My team is experiencing the same slowness. It's impacting our daily standup preparation.",
            },
        ],
        "expected": {
            "urgency": "medium",
            "product_area": "platform",
            "issue_type": "performance",
            "sentiment": "frustrated",
            "action": "route_to_specialist",
        },
    },
    # --- Ticket 16: Confused new user (onboarding) → expected LOW urgency ---
    {
        "ticket_id": "EVAL-016",
        "customer_id": "CUST-014",
        "subject": "How do I get started?",
        "messages": [
            {
                "timestamp": "2 hours ago",
                "content": "Hi, I just signed up for the free trial. Where do I start? The dashboard looks overwhelming.",
            },
            {
                "timestamp": "1 hour ago",
                "content": "I see lots of buttons but not sure what they do. Is there a tutorial or walkthrough?",
            },
            {
                "timestamp": "30 mins ago",
                "content": "Sorry for the basic questions! I'm not very tech-savvy 😅",
            },
        ],
        "expected": {
            "urgency": "low",
            "product_area": "other",
            "issue_type": "onboarding",
            "sentiment": "confused",
            "action": "auto_respond",
        },
    },
    # --- Ticket 17: Mobile app issue → expected MEDIUM urgency ---
    {
        "ticket_id": "EVAL-017",
        "customer_id": "CUST-015",
        "subject": "iOS app crashes on launch",
        "messages": [
            {
                "timestamp": "1 hour ago",
                "content": "The iOS app immediately crashes after opening. Just updated to version 3.2.1.",
            },
            {
                "timestamp": "30 mins ago",
                "content": "iPhone 14 Pro, iOS 17. It worked fine before the update.",
            },
        ],
        "expected": {
            "urgency": "medium",
            "product_area": "mobile",
            "issue_type": "bug",
            "sentiment": "frustrated",
            "action": "route_to_specialist",
        },
    },
    # --- Ticket 18: Spam/Abuse → expected LOW urgency (auto-close) ---
    {
        "ticket_id": "EVAL-018",
        "customer_id": "CUST-016",
        "subject": "FREE MONEY CLICK HERE",
        "messages": [
            {
                "timestamp": "just now",
                "content": "CLICK NOW FOR FREE MONEY $$$ http://suspicious-link.xyz",
            },
        ],
        "expected": {
            "urgency": "low",
            "product_area": "other",
            "issue_type": "spam",
            "sentiment": "neutral",
            "action": "auto_close",
        },
    },
    # --- Ticket 19: Follow-up ticket (previous issue not resolved) → expected HIGH urgency ---
    {
        "ticket_id": "EVAL-019",
        "customer_id": "CUST-017",
        "subject": "RE: Ticket #45678 - STILL NOT FIXED",
        "messages": [
            {
                "timestamp": "5 days ago",
                "content": "We submitted a ticket last week about the API timeout issue. It was marked 'resolved' but it's still happening.",
            },
            {
                "timestamp": "4 hours ago",
                "content": "Just got another timeout. This is affecting our production system now.",
            },
            {
                "timestamp": "2 hours ago",
                "content": "PLEASE escalate this. We can't wait any longer.",
            },
        ],
        "expected": {
            "urgency": "high",
            "product_area": "api",
            "issue_type": "bug",
            "sentiment": "angry",
            "action": "escalate_to_human",
        },
    },
    # --- Ticket 20: Timezone/Regional issue (APAC) → expected MEDIUM urgency ---
    {
        "ticket_id": "EVAL-020",
        "customer_id": "CUST-018",
        "subject": "Scheduled reports wrong time",
        "messages": [
            {
                "timestamp": "yesterday",
                "content": "Our scheduled reports are running at 9am instead of 6am Bangkok time.",
            },
            {
                "timestamp": "yesterday",
                "content": "Account timezone is set to Asia/Bangkok correctly.",
            },
        ],
        "expected": {
            "urgency": "medium",
            "product_area": "reporting",
            "issue_type": "bug",
            "sentiment": "neutral",
            "action": "route_to_specialist",
        },
    },
    # --- Ticket 21: Thai notification issue → expected MEDIUM urgency ---
    {
        "ticket_id": "EVAL-021",
        "customer_id": "CUST-019",
        "subject": "ไม่ได้รับอีเมลแจ้งเตือนครับ",
        "messages": [
            {
                "timestamp": "3 hours ago",
                "content": "ตั้งค่าให้ส่งอีเมลเมื่อมี task ใหม่ แต่ไม่ได้รับเลยครับ",
            },
            {
                "timestamp": "2 hours ago",
                "content": "เช็ค spam folder แล้วก็ไม่เจอ ช่วยดูหน่อยครับ",
            },
            {
                "timestamp": "1 hour ago",
                "content": "สำคัญมากครับ พลาดงานไปแล้ว 1 งาน",
            },
        ],
        "expected": {
            "urgency": "medium",
            "product_area": "notifications",
            "issue_type": "bug",
            "sentiment": "frustrated",
            "action": "route_to_specialist",
            "language": "thai",
        },
    },
    # --- Ticket 22: Team collaboration/permissions → expected HIGH urgency ---
    {
        "ticket_id": "EVAL-022",
        "customer_id": "CUST-020",
        "subject": "Team members can't access shared project",
        "messages": [
            {
                "timestamp": "2 hours ago",
                "content": "Just invited 5 team members to our project. They all see 'Access Denied' when clicking the link.",
            },
            {
                "timestamp": "1 hour ago",
                "content": "We're on Enterprise plan. All users have Enterprise licenses.",
            },
            {
                "timestamp": "30 mins ago",
                "content": "We have a deadline tomorrow and need everyone collaborating. This is blocking us.",
            },
        ],
        "expected": {
            "urgency": "high",
            "product_area": "platform",
            "issue_type": "bug",
            "sentiment": "frustrated",
            "action": "escalate_to_human",
        },
    },
    # --- Ticket 23: Dashboard reporting issue → expected MEDIUM urgency ---
    {
        "ticket_id": "EVAL-023",
        "customer_id": "CUST-021",
        "subject": "Dashboard widgets not updating",
        "messages": [
            {
                "timestamp": "6 hours ago",
                "content": "The sales widget is showing data from 3 days ago. Should be real-time.",
            },
            {
                "timestamp": "5 hours ago",
                "content": "I clicked refresh multiple times, no change. Other widgets are fine.",
            },
        ],
        "expected": {
            "urgency": "medium",
            "product_area": "reporting",
            "issue_type": "bug",
            "sentiment": "neutral",
            "action": "route_to_specialist",
        },
    },
    # --- Ticket 24: Email verification issue → expected MEDIUM urgency ---
    {
        "ticket_id": "EVAL-024",
        "customer_id": "CUST-022",
        "subject": "Can't verify email address",
        "messages": [
            {
                "timestamp": "1 day ago",
                "content": "Created an account yesterday but the verification link says 'expired' when I click it.",
            },
            {
                "timestamp": "12 hours ago",
                "content": "Requested a new verification email 3 times, never received any.",
            },
            {
                "timestamp": "6 hours ago",
                "content": "Can't access any features without verification. Please help.",
            },
        ],
        "expected": {
            "urgency": "medium",
            "product_area": "authentication",
            "issue_type": "bug",
            "sentiment": "frustrated",
            "action": "route_to_specialist",
        },
    },
    # --- Ticket 25: Data quality/Import error → expected HIGH urgency ---
    {
        "ticket_id": "EVAL-025",
        "customer_id": "CUST-023",
        "subject": "CSV import showing wrong data",
        "messages": [
            {
                "timestamp": "4 hours ago",
                "content": "Imported our customer CSV (50,000 rows). Dates are all showing as 1970-01-01.",
            },
            {
                "timestamp": "3 hours ago",
                "content": "This is critical data for our quarterly report due tomorrow.",
            },
            {
                "timestamp": "2 hours ago",
                "content": "CSV format is YYYY-MM-DD which your docs say is supported.",
            },
        ],
        "expected": {
            "urgency": "high",
            "product_area": "platform",
            "issue_type": "bug",
            "sentiment": "worried",
            "action": "escalate_to_human",
        },
    },
    # --- Ticket 26: Feature enhancement suggestion → expected LOW urgency ---
    {
        "ticket_id": "EVAL-026",
        "customer_id": "CUST-024",
        "subject": "Suggestion: Bulk export feature",
        "messages": [
            {
                "timestamp": "yesterday",
                "content": "Would be great to have a bulk export option for multiple projects at once.",
            },
            {
                "timestamp": "yesterday",
                "content": "Currently can only export one project at a time. Thanks for considering!",
            },
        ],
        "expected": {
            "urgency": "low",
            "product_area": "platform",
            "issue_type": "feature_request",
            "sentiment": "positive",
            "action": "auto_respond",
        },
    },
    # --- Ticket 27: Ambiguous urgency (could be medium or high) → expected HIGH urgency ---
    {
        "ticket_id": "EVAL-027",
        "customer_id": "CUST-025",
        "subject": "Invoice generation failed",
        "messages": [
            {
                "timestamp": "1 hour ago",
                "content": "Tried to generate invoices for our clients. Got error 'Invoice generation service unavailable'.",
            },
            {
                "timestamp": "30 mins ago",
                "content": "This is blocking our month-end billing process.",
            },
        ],
        "expected": {
            "urgency": "high",
            "product_area": "billing",
            "issue_type": "bug",
            "sentiment": "concerned",
            "action": "route_to_specialist",
        },
    },
    # --- Ticket 28: Subscription cancellation → expected LOW urgency ---
    {
        "ticket_id": "EVAL-028",
        "customer_id": "CUST-026",
        "subject": "Cancel my subscription",
        "messages": [
            {
                "timestamp": "2 hours ago",
                "content": "I'd like to cancel my Pro subscription. No longer need the service.",
            },
            {
                "timestamp": "1 hour ago",
                "content": "Please confirm when the cancellation is processed.",
            },
        ],
        "expected": {
            "urgency": "low",
            "product_area": "billing",
            "issue_type": "subscription",
            "sentiment": "neutral",
            "action": "auto_respond",
        },
    },
    # --- Ticket 29: Integration positive feedback → expected LOW urgency ---
    {
        "ticket_id": "EVAL-029",
        "customer_id": "CUST-027",
        "subject": "Slack integration working great!",
        "messages": [
            {
                "timestamp": "yesterday",
                "content": "Just wanted to say the Slack integration is working perfectly now. The fix you guys made really helped!",
            },
            {
                "timestamp": "yesterday",
                "content": "Thanks for the quick support. Much appreciated! 👍",
            },
        ],
        "expected": {
            "urgency": "low",
            "product_area": "api",
            "issue_type": "feedback",
            "sentiment": "positive",
            "action": "auto_respond",
        },
    },
    # --- Ticket 30: Thai language support question → expected LOW urgency ---
    {
        "ticket_id": "EVAL-030",
        "customer_id": "CUST-028",
        "subject": "สอบถามเรื่องภาษาไทย / Thai language support",
        "messages": [
            {
                "timestamp": "3 days ago",
                "content": "มีแผนที่จะรองรับภาษาไทยแบบเต็มรูปแบบไหมครับ ตอนนี้ใช้ได้แค่บางส่วน",
            },
            {
                "timestamp": "2 days ago",
                "content": "Is there a roadmap for full Thai language support? Currently only partial.",
            },
            {
                "timestamp": "1 day ago",
                "content": "ขอบคุณครับ / Thank you!",
            },
        ],
        "expected": {
            "urgency": "low",
            "product_area": "other",
            "issue_type": "question",
            "sentiment": "positive",
            "action": "auto_respond",
            "language": "thai",
        },
    },
]