import tempfile
import subprocess
import os
from contextlib import contextmanager
from urllib.parse import urlparse

@contextmanager
def download_repo(github_url: str):
    """
    Clones a GitHub repository into a temporary directory.
    Supports URLs like:
      - https://github.com/user/repo
      - https://github.com/user/repo/tree/branch-name
    """
    branch = None

    # Parse branch from /tree/<branch> if present
    if "/tree/" in github_url:
        base_repo_url, branch = github_url.split("/tree/", 1)
    else:
        base_repo_url = github_url

    # Ensure .git suffix for cloning (optional)
    if not base_repo_url.endswith(".git"):
        base_repo_url += ".git"

    with tempfile.TemporaryDirectory(prefix="repo_analysis_") as tmp_dir:
        try:
            print(f"Cloning {base_repo_url} into {tmp_dir}...")

            clone_cmd = ["git", "clone", "--depth", "1"]
            if branch:
                clone_cmd += ["--branch", branch]
            clone_cmd += [base_repo_url, tmp_dir]

            subprocess.run(
                clone_cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # for root, dirs, files in os.walk(tmp_dir):
            #     level = root.replace(tmp_dir, "").count(os.sep)
            #     indent = " " * level
            #     print(f"{indent}- {os.path.basename(root)}/")
            #     for f in files:
            #         print(f"{indent}  └ {f}")
            yield tmp_dir

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode().strip()
            raise RuntimeError(f"Failed to clone repository: {error_msg}")
