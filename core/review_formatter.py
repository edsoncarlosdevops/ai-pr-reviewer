"""
Formats the final review output.
"""

class ReviewFormatter:
    @staticmethod
    def format(raw_review: str) -> str:
        """
        Formats the raw review into Clark VanScoder markdown style.
        """
        # Relying on LLM to provide the correct markdown structure, wrapping here
        formatted = f"# PR Review\\n\\n{raw_review}\\n"
        return formatted
