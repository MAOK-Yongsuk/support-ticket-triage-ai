"""ChromaDB vector store wrapper for knowledge base search.

This module provides a simple interface to ChromaDB for semantic search
over knowledge base articles using OpenAI embeddings.
"""

import os
from pathlib import Path
from typing import List, Dict, Any

import chromadb
from chromadb.utils import embedding_functions


class VectorStore:
    """Wrapper for ChromaDB vector database."""
    
    def __init__(self, persist_directory: str = None, collection_name: str = "knowledge_base"):
        """Initialize ChromaDB client and collection.
        
        Args:
            persist_directory: Directory to persist ChromaDB data. 
                             Defaults to data/.chroma from env or in-memory.
            collection_name: Name of the collection to use.
        """
        if persist_directory is None:
            persist_directory = os.getenv("CHROMA_PERSIST_DIR", "data/.chroma")
        
        # Ensure persist directory exists
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client with persistent storage (new API)
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get embedding model from env
        embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        
        # Create OpenAI embedding function
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name=embedding_model
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
            metadata={"description": "Knowledge base articles for support ticket triage"}
        )
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        """Add documents to the vector store.
        
        Args:
            documents: List of document texts to add.
            metadatas: List of metadata dicts for each document.
            ids: List of unique IDs for each document.
        """
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(
        self,
        query: str,
        n_results: int = 3,
        where: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Search for similar documents using semantic similarity.
        
        Args:
            query: Search query text.
            n_results: Number of results to return.
            where: Optional metadata filter (e.g., {"category": "billing"}).
        
        Returns:
            Dict containing:
                - documents: List of matching document texts
                - metadatas: List of metadata for each match
                - distances: List of similarity distances (lower = more similar)
                - ids: List of document IDs
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )
        
        # Flatten results (query_texts is a list, so results are nested)
        return {
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "ids": results["ids"][0] if results["ids"] else [],
        }
    
    def reset(self) -> None:
        """Delete all documents from the collection."""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.create_collection(
            name=self.collection.name,
            embedding_function=self.embedding_function
        )
    
    def count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()


# Singleton instance (lazy-loaded)
_vector_store_instance = None


def get_vector_store() -> VectorStore:
    """Get or create the global VectorStore instance."""
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance
