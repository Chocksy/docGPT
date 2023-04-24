import os
import openai
import re
from typing import List
from dotenv import load_dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")

load_dotenv(verbose=True, override=True)

def get_python_files(dir_path: str) -> List[str]:
    python_files = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def get_classes_and_methods(file_path: str):
    with open(file_path, 'r') as f:
        code = f.read()

    classes = re.findall(r'class\s+(\w+)\s*[(]?\s*(\w*)\s*[)]?:', code)
    methods = re.findall(r'def\s+(\w+)\s*[(](.*)[)]', code)

    return classes, methods

def explain_code(code: str) -> str:
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Explain the following Python code:\n\n{code}\n",
        temperature=0.4,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text.strip()

def main():
    dir_path = input("Enter the directory path: ")
    python_files = get_python_files(dir_path)

    with open("documentation.md", "w") as doc_file:
        for file_path in python_files:
            classes, methods = get_classes_and_methods(file_path)
            doc_file.write(f"## File: {file_path}\n\n")

            for class_name, base_class in classes:
                class_code = f"class {class_name}({base_class}):"
                explanation = explain_code(class_code)
                doc_file.write(f"### Class: {class_name}\n{explanation}\n\n")
                doc_file.write("#### Methods:\n\n")

                for method_name, args in methods:
                    method_code = f"def {method_name}({args}):"
                    explanation = explain_code(method_code)
                    doc_file.write(f"- {method_name}\n")
                    doc_file.write(f"  - Explanation: {explanation}\n")
                    doc_file.write(f"  - Arguments: {args}\n\n")

            doc_file.write("\n\n")

if __name__ == "__main__":
    main()
