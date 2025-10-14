from designbuilder.core.cache_manager import CacheManager
from designbuilder.llm_backends.gemini import GeminiBackend
from designbuilder.prompts.prompts import Prompts
import yaml, time

class Planner:
    def __init__(self, design_doc_text, ):
        self.llm_backend = GeminiBackend()
        self.design_doc_text = design_doc_text
        self.model_name = GeminiBackend().model_name


    async def plan_all(self, components_desc_yaml='', use_cache=True, prompt_version="v0"):
        cache = CacheManager._load_cache()
        doc_hash = CacheManager._hash_doc(self.design_doc_text, self.model_name, prompt_version)

        if use_cache and doc_hash in cache:
            print("Using cached plan.")
            return cache[doc_hash]["plan"]

        print("Generating unified plan...")
        response = await self.llm_backend.send_prompt(Prompts.get_unified_plan_prompt(components_desc_yaml))

        try:
            plans = yaml.safe_load(response)
        except yaml.YAMLError as e:
            raise ValueError(f"YAML parse failed: {e}")

        cache[doc_hash] = {
            "plan": plans,
            "timestamp": time.time(),
            "model": self.model_name,
            "prompt_version": prompt_version,
        }
        CacheManager._save_cache(cache)
        return plans
