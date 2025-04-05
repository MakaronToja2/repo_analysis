import os
import ast
from analyzers.base_analyzer import CodeAnalyzer

class DocumentationAnalyzer(CodeAnalyzer):
    def analyze(self, repo_path: str) -> dict:
        total_modules = documented_modules = 0
        total_functions = documented_functions = 0
        total_classes = documented_classes = 0
        details = []
        
        # Walk through the repository and process Python files
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        tree = ast.parse(file_content)
                        
                        # Check module-level docstring
                        total_modules += 1
                        if ast.get_docstring(tree):
                            documented_modules += 1
                        
                        # Iterate over all nodes to check functions and classes
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                total_functions += 1
                                if ast.get_docstring(node):
                                    documented_functions += 1
                            elif isinstance(node, ast.ClassDef):
                                total_classes += 1
                                if ast.get_docstring(node):
                                    documented_classes += 1
                    except Exception as e:
                        details.append(f"Error processing {filepath}: {str(e)}")
        
        # Compute coverage percentages for modules, functions, and classes
        module_coverage = (documented_modules / total_modules * 100) if total_modules else 0
        function_coverage = (documented_functions / total_functions * 100) if total_functions else 0
        class_coverage = (documented_classes / total_classes * 100) if total_classes else 0
        overall_coverage = (module_coverage + function_coverage + class_coverage) / 3
        
        summary = {
            "total_modules": total_modules,
            "documented_modules": documented_modules,
            "module_coverage": f"{module_coverage:.2f}%",
            "total_functions": total_functions,
            "documented_functions": documented_functions,
            "function_coverage": f"{function_coverage:.2f}%",
            "total_classes": total_classes,
            "documented_classes": documented_classes,
            "class_coverage": f"{class_coverage:.2f}%",
            "overall_documentation_coverage": f"{overall_coverage:.2f}%"
        }
        
        return {"summary": summary, "details": details}
