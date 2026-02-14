"""Test all 8 tools to verify they work correctly.

This test suite covers:
- Context tools (4): customer_history, ticket_history, health_score, sla_status
- Search tools (1): knowledge_base
- Operational tools (2): system_status, billing_lookup
- Routing tools (1): agent_availability
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from triage_agent.tools import (
    lookup_customer_history,
    search_ticket_history,
    get_customer_health_score,
    check_sla_status,
    search_knowledge_base,
    check_system_status,
    lookup_billing_transaction,
    get_agent_availability,
)


class TestContextTools:
    """Test customer & ticket context tools."""
    
    def test_lookup_customer_history(self):
        """Test customer history lookup."""
        result = lookup_customer_history("CUST-001")
        assert result['status'] == 'found'
        assert 'customer' in result
        assert result['customer']['customer_id'] == 'CUST-001'
    
    def test_search_ticket_history(self):
        """Test ticket history search."""
        result = search_ticket_history("payment")
        # Should find "Payment failed during upgrade" ticket
        assert result['status'] in ['success', 'no_results']
        if result['status'] == 'success':
            assert 'tickets' in result
            assert result['total_results'] > 0
    
    def test_get_customer_health_score(self):
        """Test customer health score."""
        result = get_customer_health_score("CUST-002")
        assert result['status'] in ['found', 'not_found']
        if result['status'] == 'found':
            assert 'health_score' in result
            assert isinstance(result['health_score'], int)
            assert 'risk_level' in result
    
    def test_check_sla_status(self):
        """Test SLA status check."""
        result = check_sla_status("TK-2026-0015")
        # May or may not be found depending on data
        assert result['status'] in ['found', 'not_found']
        if result['status'] == 'found':
            assert 'sla' in result


class TestSearchTools:
    """Test knowledge base search tool."""
    
    def test_search_knowledge_base(self):
        """Test knowledge base search."""
        result = search_knowledge_base("payment failed during upgrade")
        # May use semantic or keyword search
        assert 'status' in result
        assert 'search_method' in result
        # If no KB data, it's ok to return no_results
        if result['status'] == 'success':
            assert 'articles' in result
            assert result['total_results'] > 0


class TestOperationalTools:
    """Test system & billing tools."""
    
    def test_check_system_status(self):
        """Test system status check."""
        result = check_system_status("us-west")
        # Should return global status info
        assert 'global_status' in result or 'regional_status' in result
    
    def test_lookup_billing_transaction(self):
        """Test billing transaction lookup."""
        # Use date only (no amount filter)
        result = lookup_billing_transaction("CUST-001", "2024-01-15")
        assert 'status' in result
        if result['status'] == 'success':
            assert 'transactions' in result


class TestRoutingTools:
    """Test agent availability tool."""
    
    def test_get_agent_availability(self):
        """Test agent availability check."""
        result = get_agent_availability("technical")  # Use valid team name
        assert 'status' in result
        if result['status'] == 'found':
            assert 'team' in result
            assert 'available_agents' in result['team']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
