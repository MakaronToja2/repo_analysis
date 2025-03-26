import argparse
from utils.repo_downloader import download_repo
from analyzers.pylint_analyzer import PylintAnalyzer
from analyzers.radon_analyzer import RadonAnalyzer
from analyzers.bandit_analyzer import BanditAnalyzer
from fpdf import FPDF
import os

def analyze_repo(repo_url: str) -> dict:
    with download_repo(repo_url) as repo_path:
        print(f"🔍 Analyzing repo: {repo_path}\n")

        analyzers = {
            "Pylint": PylintAnalyzer(),
            "Radon": RadonAnalyzer(),
            "Bandit": BanditAnalyzer()
        }

        results = {}

        for name, analyzer in analyzers.items():
            print(f"➡️  Running {name}...")
            result = analyzer.analyze(repo_path)
            if "error" in result:
                print(f"❌ {name} failed: {result['error']}")
            else:
                print(f"✅ {name} completed.\n")
            results[name] = result

        return results, repo_path

def generate_pdf_report(results: dict, output_path: str, repo_path: str):
    
    def rel(path: str):
        return os.path.relpath(path, repo_path).replace(os.sep, "/")


    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Code Quality Analysis Report", ln=True)

    for name, result in results.items():
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"{name} Analysis", ln=True)

        if "error" in result:
            pdf.set_font("Arial", "", 12)
            pdf.set_text_color(255, 0, 0)
            pdf.multi_cell(0, 10, f"Error: {result['error']}")
            pdf.set_text_color(0, 0, 0)
            continue

        # Summary Section
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Summary:", ln=True)
        pdf.set_font("Arial", "", 12)
        for key, val in result.get("summary", {}).items():
            pdf.cell(0, 10, f"- {key}: {val}", ln=True)

        # Details Section
        details = result.get("details", [])
        if isinstance(details, list) and len(details) > 0:
            pdf.ln(4)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Top Issues:", ln=True)
            pdf.set_font("Arial", "", 11)

            for issue in details[:5]:
                try:
                    if name == "Bandit":
                        pdf.multi_cell(0, 8, f"[{issue.get('issue_severity', '?')}] "
                                             f"{rel(issue.get('filename'))}:{issue.get('line_number')} - "
                                             f"{issue.get('issue_text')}")
                    elif name == "Radon":
                        pdf.multi_cell(0, 8, f"{rel(issue.get('file'))}:{issue.get('lineno')} "
                                             f"[{issue.get('rank')}] {issue.get('type')} {issue.get('name')} "
                                             f"(Complexity: {issue.get('complexity')})")
                    elif name == "Pylint":
                        pdf.multi_cell(0, 8, f"{rel(issue.get('path'))}:{issue.get('line')} "
                                             f"[{issue.get('type')}] {issue.get('message')}")
                except Exception as e:
                    pdf.multi_cell(0, 8, f"Could not render issue: {e}")

    pdf.output(output_path)
    print(f"\n📄 Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Analyze a GitHub repo with Pylint, Radon, and Bandit.")
    parser.add_argument("repo_url", help="GitHub repository URL to analyze.")
    args = parser.parse_args()

    results, repo_path = analyze_repo(args.repo_url)
    print(f"Final results: {results}")
    generate_pdf_report(results, "analysis_report.pdf", repo_path)

if __name__ == "__main__":
    main()
