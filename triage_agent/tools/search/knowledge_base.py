"""Tool: Search the knowledge base for relevant FAQ and documentation articles.

Now uses semantic search via ChromaDB + OpenAI embeddings for better relevance.
Falls back to keyword search if ChromaDB is not available.
"""

import json
from pathlib import Path
from typing import Dict, List


def search_knowledge_base(query: str) -> dict:
    """Search the knowledge base for articles relevant to a customer's issue.

    Uses semantic search (ChromaDB + OpenAI embeddings) to find the most relevant
    articles based on meaning, not just keyword matching.

    Args:
        query: A search query describing the customer's issue or keywords
               (e.g., "payment failed upgrade", "error 500 access", "dark mode").

    Returns:
        dict: A dictionary containing:
            - status: "success" or "no_results"
            - articles: List of matching articles with id, category, title, and content
            - total_results: Number of matching articles found
            - search_method: "semantic" or "keyword" (indicates which method was used)
    """
    # Try semantic search first
    try:
        return _semantic_search(query)
    except Exception as e:
        # Fallback to keyword search if ChromaDB unavailable
        print(f"[WARNING] Semantic search failed ({e}), falling back to keyword search")
        return _keyword_search(query)


def _semantic_search(query: str) -> dict:
    """Perform semantic search using ChromaDB vector store."""
    from triage_agent.tools.vector_store import get_vector_store
    
    # Get vector store instance
    vector_store = get_vector_store()
    
    # Search for top 3 most similar articles
    results = vector_store.search(query, n_results=3)
    
    if not results["ids"]:
        return {
            "status": "no_results",
            "articles": [],
            "total_results": 0,
            "search_method": "semantic",
            "message": f"No knowledge base articles found matching: '{query}'"
        }
    
    # Load article content from .txt files
    kb_dir = Path(__file__).parent.parent.parent / "data" / "knowledge_base"
    articles = []
    
    for article_id, metadata, distance in zip(
        results["ids"], 
        results["metadatas"], 
        results["distances"]
    ):
        # Read content from .txt file
        txt_file = kb_dir / f"{article_id}.txt"
        if txt_file.exists():
            with open(txt_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            
            articles.append({
                "id": article_id,
                "category": metadata.get("category", "general"),
                "title": article_id.replace("_", " ").title(),
                "content": content,
                "similarity_score": round(1 - distance, 3)  # Convert distance to similarity
            })
    
    return {
        "status": "success",
        "articles": articles,
        "total_results": len(articles),
        "search_method": "semantic"
    }


def _keyword_search(query: str) -> dict:
    """Fallback keyword-based search (original implementation).
    
    Used when ChromaDB is not available or fails.
    """
    # Load KB articles from JSON
    data_dir = Path(__file__).parent.parent.parent / "data"
    json_file = data_dir / "knowledge_base.json"
    
    if not json_file.exists():
        return {
            "status": "no_results",
            "articles": [],
            "total_results": 0,
            "search_method": "keyword",
            "message": "Knowledge base not found"
        }
    
    with open(json_file, encoding="utf-8") as f:
        knowledge_base = json.load(f)
    
    query_lower = query.lower()
    query_terms = query_lower.split()

    scored_articles = []
    for article in knowledge_base:
        score = 0
        searchable = (
            f"{article['title']} {article['content']} {' '.join(article['tags'])}"
        ).lower()

        for term in query_terms:
            if term in searchable:
                score += 1
            # Boost score for tag matches (more specific)
            if term in [tag.lower() for tag in article["tags"]]:
                score += 2

        if score > 0:
            scored_articles.append((score, article))

    # Sort by relevance score (descending) and take top 3
    scored_articles.sort(key=lambda x: x[0], reverse=True)
    top_articles = [
        {
            "id": article["id"],
            "category": article["category"],
            "title": article["title"],
            "content": article["content"],
        }
        for _, article in scored_articles[:3]
    ]

    if top_articles:
        return {
            "status": "success",
            "articles": top_articles,
            "total_results": len(top_articles),
            "search_method": "keyword"
        }

    return {
        "status": "no_results",
        "articles": [],
        "total_results": 0,
        "search_method": "keyword",
        "message": f"No knowledge base articles found matching: '{query}'",
    }
