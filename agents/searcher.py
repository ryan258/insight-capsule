# agents/searcher.py
from typing import List, Dict, Any, Optional
from core.vectorstore import VectorStore
from core.local_generation import HybridGenerator
from core.logger import setup_logger

logger = setup_logger(__name__)


class SearcherAgent:
    """
    Agent for searching and synthesizing insights from the vector store.
    Uses semantic search to find relevant insights and LLM to synthesize answers.
    """

    def __init__(self, vector_store: VectorStore, generator: HybridGenerator):
        self.vector_store = vector_store
        self.generator = generator

    def search_insights(
        self,
        query: str,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """
        Search for insights and return raw results.

        Args:
            query: Natural language search query
            n_results: Number of results to return

        Returns:
            Dictionary with search results and metadata
        """
        try:
            results = self.vector_store.search(query, n_results=n_results)

            return {
                "success": True,
                "query": query,
                "count": len(results),
                "results": results
            }

        except Exception as e:
            logger.error(f"Search failed: {e}", exc_info=True)
            return {
                "success": False,
                "query": query,
                "count": 0,
                "results": [],
                "error": str(e)
            }

    def synthesize_answer(
        self,
        query: str,
        n_results: int = 5,
        include_sources: bool = True
    ) -> str:
        """
        Search for insights and synthesize an answer using the LLM.

        Args:
            query: Natural language question
            n_results: Number of relevant insights to consider
            include_sources: Whether to include source references in the answer

        Returns:
            Synthesized answer based on relevant insights
        """
        try:
            # Search for relevant insights
            search_results = self.search_insights(query, n_results=n_results)

            if not search_results["success"] or search_results["count"] == 0:
                return "I couldn't find any relevant insights in your library for that query."

            # Build context from search results
            context_parts = []
            sources = []

            for i, result in enumerate(search_results["results"], 1):
                context_parts.append(f"[Insight {i}]\n{result['text']}")

                if include_sources and result.get("metadata"):
                    meta = result["metadata"]
                    source = f"- Insight {i}: {meta.get('title', 'Untitled')}"
                    if meta.get("timestamp"):
                        source += f" ({meta['timestamp'][:10]})"
                    sources.append(source)

            context = "\n\n".join(context_parts)

            # Create prompt for LLM
            prompt = f"""Based on the following insights from the user's personal library, answer their question.

Question: {query}

Relevant Insights:
{context}

Instructions:
- Provide a clear, concise answer based ONLY on the insights provided above
- Synthesize information across multiple insights if relevant
- If the insights don't contain enough information to answer fully, say so
- Be conversational but informative
- Do NOT make up information not present in the insights

Answer:"""

            logger.info(f"Generating answer for query: {query}")

            # Generate answer
            answer = self.generator.generate(prompt, role="writing")

            # Append sources if requested
            if include_sources and sources:
                answer += "\n\nSources:\n" + "\n".join(sources)

            return answer

        except Exception as e:
            logger.error(f"Failed to synthesize answer: {e}", exc_info=True)
            return f"An error occurred while searching your insights: {str(e)}"

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the insight library."""
        try:
            total_count = self.vector_store.get_count()

            return {
                "total_insights": total_count,
                "searchable": total_count > 0
            }

        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {
                "total_insights": 0,
                "searchable": False,
                "error": str(e)
            }
