import re
import yaml
import time
from designbuilder.core.cache_manager import CacheManager
from designbuilder.llm_backends.gemini import GeminiBackend
from designbuilder.prompts.prompts import Prompts
from designbuilder.core import parser

class Planner:
    def __init__(self, design_docs):
        self.llm_backend = GeminiBackend()
        self.design_docs = design_docs
        self.model_name = self.llm_backend.model_name

    def _extract_yaml(self, text: str) -> str:
        """Extracts a YAML code block from a string."""
        text = text.strip()
        match = re.search(r"```yaml\n(.*?)\n```", text, re.DOTALL)
        if match:
            text = match.group(1).strip()
        if text.startswith("```yaml"):
            text = text[7:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
        
        # Remove markdown-like characters that can confuse the YAML parser
        text = text.replace('*', '')
        
        return text

    async def plan_all(self, use_cache=True, prompt_version="v0"):
        # Read design docs content to generate a hash
        design_doc_text = ""
        for doc_path in self.design_docs:
            design_doc_text += await parser._read_file_content(doc_path) + "\n\n"

        cache = CacheManager._load_cache()
        doc_hash = CacheManager._hash_doc(design_doc_text)

        if use_cache and doc_hash in cache:
            print("Using cached plan.")
            return cache[doc_hash]["plan"]
        
        # Since we already have the text, we can pass it to the parser
        _, components_desc_yaml = await parser.parse_design_docs(self.design_docs, design_doc_text)

        print("Generating unified plan...")

        response = await self.llm_backend.send_prompt(Prompts.get_unified_plan_prompt(components_desc_yaml))

        cleaned_response = self._extract_yaml(response)

        try:
            plans = yaml.safe_load(cleaned_response)
        except yaml.YAMLError as e:
            raise ValueError(f"YAML parse failed: {e}")

        if plans:
            for component_plan in plans:
                if isinstance(component_plan.get("plan"), str):
                    try:
                        inner_plan_str = self._extract_yaml(component_plan["plan"])
                        component_plan["plan"] is yaml.safe_load(inner_plan_str)
                    except yaml.YAMLError as e:
                        raise ValueError(f"Failed to parse inner plan YAML for component {component_plan.get('name')}: {e}")

        cache[doc_hash] = {
            "plan": plans,
            "timestamp": time.time(),
            "model": self.model_name,
            "prompt_version": prompt_version,
        }
        CacheManager._save_cache(cache)
        return plans
