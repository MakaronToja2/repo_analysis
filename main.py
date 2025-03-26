import argparse
from utils.repo_downloader import download_repo
from analyzers.pylint_analyzer import PylintAnalyzer
from analyzers.radon_analyzer import RadonAnalyzer
from analyzers.bandit_analyzer import BanditAnalyzer

def analyze_repo(repo_url: str):
    with download_repo(repo_url) as repo_path:
        print(f"Running Pylint on: {repo_path}")
        analyzer = PylintAnalyzer()
        result = analyzer.analyze(repo_path)
        rado_analyzer = RadonAnalyzer()
        bandit_analyzer = BanditAnalyzer()
        bandit_results = bandit_analyzer.analyze(repo_path)
        print(bandit_results)
        
        # radon_results = rado_analyzer.analyze(repo_path)
        # print(radon_results)

        # if "error" in result:
        #     print(f"\n❌ Analysis failed: {result['error']}")
        #     return

        # print("\n✅ Analysis Summary:")
        # for issue_type, count in result["summary"].items():
        #     print(f"{issue_type.capitalize()}: {count}")

        # print("\nTop 5 Issues:")
        # for issue in result["details"][:5]:
        #     print(f"{issue['path']}:{issue['line']} [{issue['type']}] {issue['message']}")

def main():
    parser = argparse.ArgumentParser(description="Analyze a GitHub repo with Pylint.")
    parser.add_argument("repo_url", help="URL of the GitHub repository to analyze.")
    args = parser.parse_args()

    analyze_repo(args.repo_url)

if __name__ == "__main__":
    main()
