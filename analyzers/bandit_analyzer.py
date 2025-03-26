import json
import subprocess
from .base_analyzer import CodeAnalyzer

class BanditAnalyzer(CodeAnalyzer):
    def analyze(self, repo_path: str) -> dict:
        """
        Run Bandit on given repo_path and return security findings
        """
        try:
            print(f"Running bandit analyzer on {repo_path}")
            result = subprocess.run(
                ["bandit", "-r", repo_path, "-f", "json"],
                capture_output=True,
                text=True,
                check=False
            )
            output = result.stdout
            bandit_results = json.loads(output)
        except subprocess.CalledProcessError as e:
            return {"error": f"Bandit failed: {e.stderr.strip()}"}
        except json.JSONDecodeError:
            return {"error": "Failed to parse Bandit output."}

        summary = self._generate_summary(bandit_results)
        details = bandit_results.get("results", [])
        print(f"This is the summary: {summary}")
        if not summary and not details:
            return {"error": "No issues found or not analyzable files in the repo"}
        return {
            "summary": summary,
            "details": details
        }

    def _generate_summary(self, data: dict) -> dict:
        summary = {}
        for issue in data.get("results", []):
            severity = issue.get("issue_severity", "UNSPECIFIED")
            summary[severity] = summary.get(severity, 0) + 1
        return summary