"""Mock customer records and ticket history."""

CUSTOMER_RECORDS: dict[str, dict] = {
    "CUST-001": {
        "customer_id": "CUST-001",
        "name": "Alice Johnson",
        "email": "alice.johnson@email.com",
        "plan": "free",
        "region": "US",
        "tenure_months": 4,
        "seats": 1,
        "monthly_spend": 0.0,
        "previous_tickets": [],
        "notes": "First time contacting support. Attempted upgrade to Pro.",
    },
    "CUST-002": {
        "customer_id": "CUST-002",
        "name": "Somchai Thongdee",
        "email": "somchai.t@enterprise-corp.co.th",
        "plan": "enterprise",
        "region": "Thailand",
        "tenure_months": 8,
        "seats": 45,
        "monthly_spend": 2250.00,
        "previous_tickets": [
            {
                "ticket_id": "TK-2025-0042",
                "date": "2025-09-15",
                "issue": "SSO configuration help",
                "resolution": "Resolved — guided through SAML setup",
                "satisfaction": "positive",
            },
        ],
        "notes": "Enterprise customer, Thailand region. High-value account. First critical issue.",
    },
    "CUST-003": {
        "customer_id": "CUST-003",
        "name": "Emily Chen",
        "email": "emily.chen@startup.io",
        "plan": "pro",
        "region": "US",
        "tenure_months": 5,
        "seats": 1,
        "monthly_spend": 29.99,
        "previous_tickets": [],
        "notes": "Active daily user. No previous support tickets.",
    },
}
