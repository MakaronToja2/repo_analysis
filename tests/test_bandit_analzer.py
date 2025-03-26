from utils.repo_downloader import download_repo
from analyzers.bandit_analyzer import BanditAnalyzer

def test_bandit_analyzer_returns_valid_data():
    repo_url = "https://github.com/MakaronToja2/repo_analysis_test_repo/tree/bandit_issue"

    with download_repo(repo_url) as repo_path:
        analyzer = BanditAnalyzer()
        result = analyzer.analyze(repo_path)

        assert "error" not in result
        assert isinstance(result["summary"], dict), "Summary should be a dict"
        assert isinstance(result["details"], list), "Details should be a list"

def test_bandit_analyzer_returns_repo_with_no_issues():
    repo_url = "https://github.com/MakaronToja2/repo_analysis_test_repo"

    with download_repo(repo_url) as repo_path:
        analyzer = BanditAnalyzer()
        result = analyzer.analyze(repo_path)

        assert "error" in result
        assert result["error"] == "No issues found or not analyzable files in the repo"