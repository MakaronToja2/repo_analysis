import io
import json
from pylint.lint import Run
from pylint.reporters.json_reporter import JSONReporter
from .base_analyzer import CodeAnalyzer

class PylintAnalyzer(CodeAnalyzer):
    def analyze(self, repo_path: str) -> dict:
        """
        Run pylint on the given repo_path and return parsed results
        """
        output_stream = io.StringIO()
        reporter = JSONReporter(output=output_stream)

        try:
            Run([repo_path], reporter=reporter, do_exit=False)
        except Exception as e:
            return {"error:" f"Pylint analysis failed {str(e)}"}
        
        output = output_stream.getvalue()
        try:
            pylint_results = json.loads(output)
        except json.JSONDecodeError:
            return {"error": "Failed to parse pylint output."}
        
        summary = self._generate_sumary(pylint_results)

        return {
            "summary": summary,
            "details": pylint_results,
        }
    
    def _generate_summary(self, results: list) -> dict:
        """
        Generate a suary of the issue by type.
        """