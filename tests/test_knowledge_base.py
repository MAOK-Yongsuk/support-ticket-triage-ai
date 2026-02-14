"""Tests for knowledge base search tool."""

from triage_agent.tools.search.knowledge_base import search_knowledge_base


class TestSearchKnowledgeBase:
    """Test suite for the search_knowledge_base tool."""

    def test_search_payment_keywords(self):
        """Should return billing articles for payment-related queries."""
        result = search_knowledge_base("payment failed upgrade")
        assert result["status"] == "success"
        assert result["total_results"] > 0
        assert any("billing" in a["category"] for a in result["articles"])

    def test_search_error_500(self):
        """Should return system articles for error 500 queries."""
        result = search_knowledge_base("error 500 server down")
        assert result["status"] == "success"
        assert any("system" in a["category"] for a in result["articles"])

    def test_search_dark_mode(self):
        """Should return feature articles for dark mode queries."""
        result = search_knowledge_base("dark mode theme appearance")
        assert result["status"] == "success"
        assert any("features" in a["category"] for a in result["articles"])

    def test_search_no_results(self):
        """Should return no_results for unrelated queries."""
        result = search_knowledge_base("xyzzy quantum teleportation")
        assert result["status"] == "no_results"
        assert result["total_results"] == 0
        assert result["articles"] == []

    def test_search_returns_max_three(self):
        """Should return at most 3 articles."""
        result = search_knowledge_base("billing payment charge refund upgrade plan")
        assert result["total_results"] <= 3

    def test_search_result_structure(self):
        """Each article should have id, category, title, content."""
        result = search_knowledge_base("payment")
        if result["status"] == "success":
            for article in result["articles"]:
                assert "id" in article
                assert "category" in article
                assert "title" in article
                assert "content" in article
