import argparse
import os
from datetime import datetime
from utils.repo_downloader import download_repo
from analyzers.pylint_analyzer import PylintAnalyzer
from analyzers.radon_analyzer import RadonAnalyzer
from analyzers.bandit_analyzer import BanditAnalyzer
from fpdf import FPDF

def analyze_repo(repo_url: str) -> tuple:
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
    # Helper function to get paths relative to the repo root
    def rel(path: str):
        return os.path.relpath(path, repo_path).replace(os.sep, "/")
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Code Quality Analysis Report", ln=True)

    # Process each analyzer's result
    for name, result in results.items():
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"{name} Analysis", ln=True)

        # If the analyzer returned an error, display it in red
        if "error" in result:
            pdf.set_font("Arial", "", 12)
            pdf.set_text_color(255, 0, 0)
            pdf.multi_cell(0, 10, f"Error: {result['error']}")
            pdf.set_text_color(0, 0, 0)
            continue

        # Summary section
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Summary:", ln=True)
        pdf.set_font("Arial", "", 12)
        for key, val in result.get("summary", {}).items():
            pdf.cell(0, 10, f"- {key}: {val}", ln=True)

        # Details (Top Issues) section
        details = result.get("details", [])
        if isinstance(details, list) and len(details) > 0:
            # Sort issues according to analyzer-specific severity:
            if name == "Bandit":
                # Bandit: sort descending by issue_severity ("HIGH" > "MEDIUM" > "LOW")
                severity_order = {"HIGH": 2, "MEDIUM": 1, "LOW": 0}
                sorted_details = sorted(details, key=lambda i: severity_order.get(i.get("issue_severity", "LOW"), 0), reverse=True)
            elif name == "Radon":
                # Radon: sort descending by rank (F > E > D > C > B > A)
                rank_order = {"F": 5, "E": 4, "D": 3, "C": 2, "B": 1, "A": 0}
                sorted_details = sorted(details, key=lambda i: rank_order.get(i.get("rank", "A"), 0), reverse=True)
            elif name == "Pylint":
                # Pylint: sort descending by type severity (warning > refactor > convention)
                pylint_order = {"error": 3, "warning": 2, "refactor": 1, "convention": 0}
                sorted_details = sorted(details, key=lambda i: pylint_order.get(i.get("type", "convention"), 0), reverse=True)
            else:
                sorted_details = details

            pdf.ln(4)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Top Issues:", ln=True)
            pdf.set_font("Arial", "", 11)

            # Display only the top 5 sorted issues
            for issue in sorted_details[:5]:
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
    output_filename = f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    generate_pdf_report(results, output_filename, repo_path)

if __name__ == "__main__":
    main()
