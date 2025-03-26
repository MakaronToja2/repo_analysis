import os
import pytest
from utils.repo_downloader import download_repo

def test_download_repo_success():
    test_repo_url = "https://github.com/octocat/Hello-World"

    with download_repo(test_repo_url) as repo_path:
        assert os.path.exists(repo_path), "Repo path does not exist"
        assert os.path.isdir(repo_path), "Repo path is not a directory"

        files = os.listdir(repo_path)
        assert len(files) > 0, "Repo path is empty after cloning"

def test_download_repo_failed():
    invalid_url = "https://github.com/invalid/invalid-repo-url"

    with pytest.raises(RuntimeError) as exc_info:
        with download_repo(invalid_url):
            pass

    assert "Failed to clone repository" in str(exc_info.value)

@pytest.mark.integration
def test_download_specific_branch():
    repo_url_with_branch = "https://github.com/MakaronToja2/repo_analysis_test_repo/tree/bandit_issue"

    with download_repo(repo_url_with_branch) as repo_path:
        assert os.path.exists(repo_path), "Repo pathj does not exist"
        assert os.path.isdir(repo_path), "Repo path is not a directory"
        files = os.listdir(repo_path)
        assert len(files) > 0, "Repo path is empty after cloning"