"""Ingest knowledge base articles from .txt files into ChromaDB.

This script reads all .txt files from data/knowledge_base/, generates
embeddings using OpenAI API, and stores them in ChromaDB for semantic search.

Run this script once after setting up the knowledge base files.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import vector store
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from triage_agent.tools.search.vector_store import VectorStore


def extract_metadata_from_filename(filename: str) -> dict:
    """Extract category and generate tags from filename.
    
    Args:
        filename: Filename without extension (e.g., "billing_payment_failure")
    
    Returns:
        Dict with category and tags
    """
    parts = filename.split("_")
    category = parts[0] if parts else "general"
    tags = parts  # All parts become tags
    
    return {
        "category": category,
        "tags": " ".join(tags),  # Store as space-separated string
        "article_id": filename
    }


def main():
    # Paths
    project_root = Path(__file__).parent.parent
    kb_dir = project_root / "data" / "knowledge_base"
    
    if not kb_dir.exists():
        print(f"[ERROR] Knowledge base directory not found: {kb_dir}")
        return
    
    # Find all .txt files
    txt_files = list(kb_dir.glob("*.txt"))
    if not txt_files:
        print(f"[ERROR] No .txt files found in {kb_dir}")
        return
    
    print(f"Found {len(txt_files)} articles to ingest")
    
    # Initialize vector store
    print("Initializing ChromaDB...")
    vector_store = VectorStore()
    
    # Reset collection (optional - comment out to keep existing data)
    print("Resetting collection...")
    vector_store.reset()
    
    # Prepare data for ingestion
    documents = []
    metadatas = []
    ids = []
    
    for txt_file in txt_files:
        # Read content
        with open(txt_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        # Extract metadata from filename
        filename_without_ext = txt_file.stem
        metadata = extract_metadata_from_filename(filename_without_ext)
        
        # Add to lists
        documents.append(content)
        metadatas.append(metadata)
        ids.append(filename_without_ext)
        
        print(f"  - {filename_without_ext} ({metadata['category']})")
    
    # Ingest into ChromaDB
    print(f"\nGenerating embeddings and storing in ChromaDB...")
    vector_store.add_documents(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    # Verify
    count = vector_store.count()
    print(f"\n[SUCCESS] Ingested {count} articles into ChromaDB")
    print(f"Vector store location: {os.getenv('CHROMA_PERSIST_DIR', 'data/.chroma')}")
    
    # Test search
    print("\n--- Testing semantic search ---")
    test_query = "my payment failed"
    results = vector_store.search(test_query, n_results=2)
    print(f"Query: '{test_query}'")
    print(f"Top results:")
    for i, (doc_id, distance) in enumerate(zip(results["ids"], results["distances"]), 1):
        print(f"  {i}. {doc_id} (distance: {distance:.4f})")


if __name__ == "__main__":
    main()
