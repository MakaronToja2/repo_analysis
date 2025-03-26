import os
from analyzers.radon_analyzer import RadonAnalyzer
from utils.repo_downloader import download_repo

def test_radon_analyzer_detect_complexity():
    test_repo_url = "https://github.com/MakaronToja2/repo_analysis_test_repo"

    with download_repo(test_repo_url) as repo_path:
        analyzer = RadonAnalyzer()
        result = analyzer.analyze(repo_path)

        assert "error" not in result, f"Pylint failed with error: {result['error']}"
        assert isinstance(result["summary"], dict), "Summary should be a dict"
        assert isinstance(result["details"], list), "Details should be a list"
        assert any("complexity" in r for r in result["details"]), "No complexity data found"

def test_radon_analyzer_handles_empty_files(tmp_path):
    empty_file = tmp_path / "empty.py"
    empty_file.write_text("")

    analyzer = RadonAnalyzer()
    result = analyzer.analyze(str(tmp_path))
    assert "error" not in result, f"Pylint failed with error: {result['error']}"
    assert isinstance(result["summary"], dict), "Summary should be a dict"
    assert isinstance(result["details"], list), "Details should be a list"