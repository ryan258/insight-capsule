"""
Vector store for semantic search across insight capsules.
Uses ChromaDB for local vector storage and sentence-transformers for embeddings.
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from config.settings import DATA_DIR
from core.logger import setup_logger

logger = setup_logger(__name__)


class VectorStore:
    """
    Manages vector embeddings and semantic search for insight capsules.
    Uses a local sentence-transformer model for privacy and offline operation.
    """

    def __init__(
        self,
        persist_directory: Optional[Path] = None,
        model_name: str = "all-MiniLM-L6-v2"  # Fast, efficient, 384-dim embeddings
    ):
        """
        Initialize the vector store.

        Args:
            persist_directory: Directory to persist ChromaDB data
            model_name: Sentence-transformer model to use for embeddings
        """
        self.persist_directory = persist_directory or (DATA_DIR / "vectorstore")
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        logger.info(f"Initializing vector store at: {self.persist_directory}")
        logger.info(f"Loading embedding model: {model_name}")

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Load sentence-transformer model
        try:
            self.embedding_model = SentenceTransformer(model_name)
            logger.info(f"Embedding model loaded: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}", exc_info=True)
            raise

        # Get or create collection
        self.collection_name = "insights"
        try:
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Insight capsules and transcripts"}
            )
            logger.info(f"Collection '{self.collection_name}' ready")
        except Exception as e:
            logger.error(f"Failed to create collection: {e}", exc_info=True)
            raise

    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text."""
        try:
            embedding = self.embedding_model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}", exc_info=True)
            raise

    def add_insight(
        self,
        insight_id: str,
        transcript: str,
        capsule: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add an insight to the vector store.

        Args:
            insight_id: Unique identifier for the insight (e.g., timestamp-based)
            transcript: Original voice transcript
            capsule: Generated insight capsule
            metadata: Additional metadata (title, tags, timestamp, etc.)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Combine transcript and capsule for richer search
            combined_text = f"{transcript}\n\n{capsule}"

            # Generate embedding
            embedding = self._generate_embedding(combined_text)

            # Prepare metadata
            meta = metadata or {}
            meta.update({
                "added_at": datetime.now().isoformat(),
                "has_transcript": bool(transcript),
                "has_capsule": bool(capsule)
            })

            # Add to collection
            self.collection.add(
                ids=[insight_id],
                embeddings=[embedding],
                documents=[combined_text],
                metadatas=[meta]
            )

            logger.info(f"Added insight to vector store: {insight_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to add insight to vector store: {e}", exc_info=True)
            return False

    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant insights using semantic similarity.

        Args:
            query: Natural language query
            n_results: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of matching insights with metadata and scores
        """
        try:
            # Generate query embedding
            query_embedding = self._generate_embedding(query)

            # Search collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata,
                include=["documents", "metadatas", "distances"]
            )

            # Format results
            formatted_results = []
            if results and results["ids"] and len(results["ids"][0]) > 0:
                for i in range(len(results["ids"][0])):
                    formatted_results.append({
                        "id": results["ids"][0][i],
                        "text": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i],
                        # Convert distance to similarity score (0-1)
                        "similarity": 1.0 / (1.0 + results["distances"][0][i])
                    })

            logger.info(f"Search found {len(formatted_results)} results for query: '{query[:50]}...'")
            return formatted_results

        except Exception as e:
            logger.error(f"Search failed: {e}", exc_info=True)
            return []

    def get_count(self) -> int:
        """Get the total number of insights in the store."""
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Failed to get count: {e}")
            return 0

    def delete_insight(self, insight_id: str) -> bool:
        """Delete an insight from the vector store."""
        try:
            self.collection.delete(ids=[insight_id])
            logger.info(f"Deleted insight: {insight_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete insight: {e}", exc_info=True)
            return False

    def reset(self) -> bool:
        """Reset the entire collection (use with caution!)."""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Insight capsules and transcripts"}
            )
            logger.warning("Vector store has been reset")
            return True
        except Exception as e:
            logger.error(f"Failed to reset vector store: {e}", exc_info=True)
            return False
