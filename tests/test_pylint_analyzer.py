import os
from services.pylint_analyzer import PylintAnalyzer

def test_pylint_on_sample_repo():
    repo_path = os.path.abspath("sample_repo")
    analyzer = PylintAnalyzer()
    result = analyzer.analyze(repo_path)