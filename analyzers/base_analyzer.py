from abc import ABC, abstractmethod

class CodeAnalyzer(ABC):
    @abstractmethod
    def analyze(self, repo_path: str) -> dict:
        """Run analysis on the given repository path and return results."""
        pass
