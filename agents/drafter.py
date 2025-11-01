# agents/drafter.py
from typing import Dict, Any, Optional
from core.local_generation import HybridGenerator
from core.logger import setup_logger

logger = setup_logger(__name__)


class DrafterAgent:
    """
    Agent for generating blog post outlines and first drafts from insight capsules.
    Helps bridge the gap from raw insight to published content.
    """

    def __init__(self, generator: HybridGenerator):
        self.generator = generator

    def generate_blog_outline(
        self,
        capsule: str,
        transcript: Optional[str] = None,
        num_points: int = 5
    ) -> str:
        """
        Generate a blog post outline from an insight capsule.

        Args:
            capsule: The insight capsule to build upon
            transcript: Optional original transcript for additional context
            num_points: Number of main points in the outline

        Returns:
            A structured blog post outline
        """
        context = f"Original thought:\n{transcript}\n\n" if transcript else ""

        prompt = f"""You are a content strategist helping to turn an insight into a blog post outline.

{context}Insight:
\"\"\"{capsule}\"\"\"

Create a {num_points}-point blog post outline based on this insight. The outline should:
- Have a compelling title
- Include {num_points} main sections with brief descriptions
- Be suitable for an evergreen guide or educational content
- Target readers who want practical, actionable information

Format the outline clearly with:
# Title
## Introduction (brief)
## Main Points (numbered 1-{num_points})
## Conclusion (brief)

Blog Post Outline:"""

        logger.info("Generating blog outline")
        return self.generator.generate(prompt, role="writing")

    def generate_first_draft(
        self,
        capsule: str,
        outline: Optional[str] = None,
        transcript: Optional[str] = None,
        target_words: int = 500
    ) -> str:
        """
        Generate a first draft of a blog post from an insight capsule.

        Args:
            capsule: The insight capsule to build upon
            outline: Optional outline to follow
            transcript: Optional original transcript for additional context
            target_words: Target word count for the draft

        Returns:
            A first draft of the blog post
        """
        context_parts = []

        if transcript:
            context_parts.append(f"Original thought:\n{transcript}")

        if outline:
            context_parts.append(f"Outline to follow:\n{outline}")

        context = "\n\n".join(context_parts) + "\n\n" if context_parts else ""

        prompt = f"""You are a content writer helping to turn an insight into a blog post first draft.

{context}Insight:
\"\"\"{capsule}\"\"\"

Write a first draft of approximately {target_words} words based on this insight.
{"Follow the outline provided above. " if outline else ""}
The draft should:
- Be conversational and engaging
- Focus on practical, actionable information
- Include specific examples where relevant
- Be suitable for an evergreen guide format
- Avoid jargon and be accessible to a general audience

Write the complete first draft (approximately {target_words} words):"""

        logger.info("Generating first draft")
        return self.generator.generate(prompt, role="writing")

    def generate_key_takeaways(
        self,
        capsule: str,
        num_takeaways: int = 3
    ) -> str:
        """
        Generate key takeaways or summary points from an insight capsule.

        Args:
            capsule: The insight capsule to summarize
            num_takeaways: Number of key takeaways to generate

        Returns:
            A list of key takeaways
        """
        prompt = f"""Based on the following insight, generate {num_takeaways} key takeaways.
Make them concise, actionable, and memorable.

Insight:
\"\"\"{capsule}\"\"\"

Format as a numbered list.

Key Takeaways:"""

        logger.info("Generating key takeaways")
        return self.generator.generate(prompt, role="writing")

    def expand_section(
        self,
        section_title: str,
        capsule: str,
        target_words: int = 200
    ) -> str:
        """
        Expand a specific section based on the insight capsule.

        Args:
            section_title: The section to expand
            capsule: The insight capsule for context
            target_words: Target word count for the section

        Returns:
            Expanded section content
        """
        prompt = f"""Based on the following insight, write an expanded section for: "{section_title}"

Insight:
\"\"\"{capsule}\"\"\"

Write approximately {target_words} words for this section. Make it practical and engaging.

{section_title}:"""

        logger.info(f"Expanding section: {section_title}")
        return self.generator.generate(prompt, role="writing")
