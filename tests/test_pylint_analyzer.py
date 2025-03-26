import os
from analyzers.pylint_analyzer import PylintAnalyzer

def test_pylint_on_sample_repo():
    repo_path = os.path.abspath("repo_analysis_test_repo")
    analyzer = PylintAnalyzer()
    result = analyzer.analyze(repo_path)

    assert "error" not in result, f"Pylint failed with error: {result['error']}"
    assert isinstance(result["summary"], dict), "Summary should be a dict"
    assert len(result["summary"]) >0, "Summary should contain at least one issue type"
    assert isinstance(result["details"], list), "Details should be a list"
    assert len(result["details"]) > 0, "Pylint should detect issues in non-PEP8 code repo"