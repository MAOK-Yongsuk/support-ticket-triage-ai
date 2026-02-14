"""Test embeddings and semantic search functionality.

Run this to verify ChromaDB is working correctly.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from triage_agent.tools.search.vector_store import get_vector_store


def test_vector_store_initialization():
    """Test that vector store initializes correctly."""
    vector_store = get_vector_store()
    assert vector_store is not None
    assert vector_store.count() > 0, "Vector store is empty. Run: uv run python scripts/ingest_kb.py"


def test_semantic_search():
    """Test semantic search returns relevant results."""
    vector_store = get_vector_store()
    
    # Test query
    results = vector_store.search("payment failed during upgrade", n_results=3)
    
    # Verify results
    assert results["ids"], "No results returned"
    assert len(results["ids"]) > 0, "Expected at least 1 result"
    assert "billing" in results["ids"][0].lower(), "Expected billing-related result"


def test_search_quality():
    """Test that semantic search returns high-quality matches."""
    vector_store = get_vector_store()
    
    test_cases = [
        ("payment failed", "billing"),
        ("server error 500", "system"),
        ("dark mode", "features"),
    ]
    
    for query, expected_category in test_cases:
        results = vector_store.search(query, n_results=1)
        assert results["ids"], f"No results for query: {query}"
        
        # Check that top result is relevant
        top_result = results["ids"][0]
        assert expected_category in top_result.lower(), \
            f"Expected '{expected_category}' in result for query '{query}', got: {top_result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
