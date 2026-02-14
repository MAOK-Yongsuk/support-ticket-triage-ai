"""Tests for customer history lookup tool."""

from triage_agent.tools.context.customer_history import lookup_customer_history


class TestLookupCustomerHistory:
    """Test suite for the lookup_customer_history tool."""

    def test_lookup_existing_customer(self):
        """Should return customer data for a valid ID."""
        result = lookup_customer_history("CUST-001")
        assert result["status"] == "found"
        assert result["customer"]["customer_id"] == "CUST-001"
        assert result["customer"]["plan"] == "free"

    def test_lookup_enterprise_customer(self):
        """Should return full enterprise customer profile."""
        result = lookup_customer_history("CUST-002")
        assert result["status"] == "found"
        customer = result["customer"]
        assert customer["plan"] == "enterprise"
        assert customer["region"] == "Thailand"
        assert customer["seats"] == 45
        assert customer["monthly_spend"] > 0

    def test_lookup_pro_customer(self):
        """Should return pro customer with no previous tickets."""
        result = lookup_customer_history("CUST-003")
        assert result["status"] == "found"
        assert result["customer"]["plan"] == "pro"
        assert result["customer"]["total_previous_tickets"] == 0

    def test_lookup_nonexistent_customer(self):
        """Should return not_found for unknown customer IDs."""
        result = lookup_customer_history("CUST-999")
        assert result["status"] == "not_found"
        assert "message" in result

    def test_customer_has_previous_tickets(self):
        """Enterprise customer should have previous ticket history."""
        result = lookup_customer_history("CUST-002")
        assert result["customer"]["total_previous_tickets"] > 0
        assert len(result["customer"]["previous_tickets"]) > 0

    def test_customer_result_structure(self):
        """Customer result should contain all expected fields."""
        result = lookup_customer_history("CUST-001")
        customer = result["customer"]
        expected_fields = [
            "customer_id", "name", "plan", "region",
            "tenure_months", "seats", "monthly_spend",
            "previous_tickets", "total_previous_tickets", "notes",
        ]
        for field in expected_fields:
            assert field in customer, f"Missing field: {field}"
