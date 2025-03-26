import os
from radon.complexity import cc_visit, cc_rank
from radon.visitors import ComplexityVisitor
from .base_analyzer import CodeAnalyzer

class RadonAnalyzer(CodeAnalyzer):
    def analyze(self, repo_path: str) -> dict:
        """
        Analyze the code complexity in the repo using radon
        """
        results = []
        try:
            for root, _, files in os.walk(repo_path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                source_code = f.read()
                            analyzed = cc_visit(source_code)
                            print(f"This analyzed {analyzed}")
                            for block in analyzed:
                                results.append({
                                    "file": file_path,
                                    "name": block.name,
                                    "complexity": block.complexity,
                                    "type": type(block).__name__.lower(),
                                    "lineno": block.lineno,
                                    "rank": cc_rank(block.complexity), 
                                })
                        except Exception as e:
                            results.append({
                                "file": file_path,
                                "error": str(e)
                            })
        except Exception as e:
            return {"error": f"Radon analysis failed: {str(e)}"}
        print(f"this is our results: {results}")
        summary = self._generate_summary(results)
        print(f"this is summary: {summary}")
        return {
            "summary": summary,
            "details": results
        }
        
    
    def _generate_summary(self, results: list) -> dict:
        """
        Summarize number of code blocks by complexity rank
        """
        rank_counts = {}
        for res in results:
            if "rank" in res:
                rank = res["rank"]
                rank_counts[rank] = rank_counts.get(rank, 0) + 1
        return rank_counts