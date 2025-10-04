"""
Design Document Parser

Extracts software components and their requirements from
design documents using an LLM.
"""
import os
import json
import docx
from pypdf import PdfReader
from designbuilder.llm_backends.gemini import GeminiBackend

async def _read_file_content(file_path: str) -> str:
    """Reads the content of a file based on its extension."""
    _, extension = os.path.splitext(file_path)
    content = ""

    try:
        if extension in [".md", ".mdx"]:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        elif extension == ".pdf":
            reader = PdfReader(file_path)
            for page in reader.pages:
                content += page.extract_text() or ''
        elif extension == ".docx":
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                content += para.text + "\n"
        else:
            print(f"Warning: Unsupported file type: {extension}. Reading as plain text.")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return content

async def parse_design_docs(design_docs: list[str]) -> list[dict]:
    """
    Reads design documents, uses an LLM to extract components,
    and returns them as a list of dictionaries.
    """
    print(f"Parsing design documents: {design_docs}")
    
    full_text = ""
    for doc_path in design_docs:
        full_text += await _read_file_content(doc_path) + "\n\n"

    if not full_text.strip():
        return []

    prompt = f"""Analyze the following system design document(s) and extract the architectural components.

For each component, provide its name, a detailed description of its responsibilities, and the programming language or technology it uses.

Please provide the output in JSON format as a list of objects, where each object has the keys "name", "description", and "language".

---

{full_text}
"""

    llm_backend = GeminiBackend()
    json_output = await llm_backend.generate_content(prompt)

    try:
        # The LLM might return the JSON within a code block, so we need to extract it.
        if "```json" in json_output:
            json_output = json_output.split("```json")[1].split("```")[0]
        components = json.loads(json_output)
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error parsing JSON from LLM: {e}")
        print(f"LLM output:\n{json_output}")
        components = []

    return components