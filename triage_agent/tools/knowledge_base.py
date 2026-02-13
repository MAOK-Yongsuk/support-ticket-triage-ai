"""Tool: Search the knowledge base for relevant FAQ and documentation articles."""

import json
from pathlib import Path

# Load KB articles from JSON
_DATA_DIR = Path(__file__).parent.parent.parent / "data"
with open(_DATA_DIR / "knowledge_base.json", encoding="utf-8") as f:
    KNOWLEDGE_BASE = json.load(f)


def search_knowledge_base(query: str) -> dict:
    """Search the knowledge base for articles relevant to a customer's issue.

    Use this tool to find FAQ articles, troubleshooting guides, and documentation
    that may help resolve the customer's problem or provide relevant information
    for your triage decision.

    Args:
        query: A search query describing the customer's issue or keywords
               (e.g., "payment failed upgrade", "error 500 access", "dark mode").

    Returns:
        dict: A dictionary containing:
            - status: "success" or "no_results"
            - articles: List of matching articles with id, category, title, and content
            - total_results: Number of matching articles found
    """
    query_lower = query.lower()
    query_terms = query_lower.split()

    scored_articles = []
    for article in KNOWLEDGE_BASE:
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
        }

    return {
        "status": "no_results",
        "articles": [],
        "total_results": 0,
        "message": f"No knowledge base articles found matching: '{query}'",
    }
