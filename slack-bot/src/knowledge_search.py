"""
Knowledge Base Search Module
Searches local intuit-boom project files for relevant information.
"""

import os
from pathlib import Path
from typing import List, Dict


class KnowledgeSearch:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.index = self._build_index()

    def _build_index(self) -> Dict[str, str]:
        """Build index of all searchable files."""
        index = {}
        extensions = {".md", ".txt", ".py", ".json"}
        skip_dirs = {
            ".git",
            "__pycache__",
            ".ruff_cache",
            "chrome_profile_sheets",
            "chrome_profile_sheets2",
            "chrome_gsheets",
            "screenshots",
        }

        for root, dirs, files in os.walk(self.base_path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]

            for file in files:
                if Path(file).suffix in extensions:
                    filepath = Path(root) / file
                    try:
                        content = filepath.read_text(encoding="utf-8", errors="ignore")
                        index[str(filepath)] = content
                    except Exception:
                        pass

        return index

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search knowledge base for relevant content."""
        results = []
        query_terms = query.lower().split()

        for filepath, content in self.index.items():
            content_lower = content.lower()

            # Score based on term matches
            score = sum(1 for term in query_terms if term in content_lower)

            if score > 0:
                # Extract relevant snippets
                snippets = self._extract_snippets(content, query_terms)
                results.append({"file": filepath, "score": score, "snippets": snippets[:3]})

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]

    def _extract_snippets(self, content: str, terms: List[str], context_lines: int = 2) -> List[str]:
        """Extract snippets around matching terms."""
        lines = content.split("\n")
        snippets = []

        for i, line in enumerate(lines):
            if any(term in line.lower() for term in terms):
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                snippet = "\n".join(lines[start:end])
                if snippet not in snippets:
                    snippets.append(snippet)

        return snippets

    def get_context_summary(self, query: str) -> str:
        """Get a formatted summary of relevant knowledge for a query."""
        results = self.search(query)

        if not results:
            return "No relevant information found in knowledge base."

        summary_parts = ["## Knowledge Base Results\n"]

        for result in results:
            filename = Path(result["file"]).name
            summary_parts.append(f"### {filename} (relevance: {result['score']})")
            for snippet in result["snippets"]:
                summary_parts.append(f"```\n{snippet[:500]}\n```")
            summary_parts.append("")

        return "\n".join(summary_parts)


# Singleton instance
_search_instance = None


def get_searcher(base_path: Path = None) -> KnowledgeSearch:
    global _search_instance
    if _search_instance is None:
        if base_path is None:
            base_path = Path(__file__).parent.parent.parent
        _search_instance = KnowledgeSearch(base_path)
    return _search_instance
