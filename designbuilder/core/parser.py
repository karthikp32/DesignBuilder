"""
Design Document Parser

Extracts software components and their requirements from
design documents using an LLM.
"""
import os
import yaml
import docx
from pypdf import PdfReader
from designbuilder.llm_backends.gemini import GeminiBackend
from designbuilder.llm_backends.gpt4_turbo import GPT4TurboBackend
from designbuilder.prompts.prompts import Prompts

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


async def parse_design_docs(design_docs: list[str], design_doc_text: str = None) -> str:
    """
    Reads design documents, uses an LLM to extract components,
    and returns them as a YAML formatted string.
    """
    print(f"Parsing design documents: {design_docs}")

    full_text = design_doc_text
    if not full_text:
        for doc_path in design_docs:
            full_text += await _read_file_content(doc_path) + "\n\n"
    
    #TODO: modify this to return list of full texts
    if not full_text.strip():
        return ""


    prompt = Prompts.get_design_doc_extraction_prompt(full_text)

    llm_backend = GeminiBackend()
    yaml_output = await llm_backend.send_prompt(prompt)

    try:
        # The LLM might return the YAML within a code block, so we need to extract it.
        if "```yaml" in yaml_output:
            yaml_output = yaml_output.split("```yaml")[1].split("```")[0]
        components = yaml.safe_load(yaml_output)
    except (yaml.YAMLError, IndexError) as e:
        print(f"Error parsing YAML from LLM: {e}")
        print(f"LLM output:\n{yaml_output}")
        components = []

    return full_text, yaml.dump(components)