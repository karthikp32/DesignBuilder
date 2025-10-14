import yaml, time, os, hashlib, json

CACHE_FILE = "/home/karthik/repos/DesignBuilder/designbuilder/cache/plan_cache.json"

class CacheManager:

    @staticmethod
    def _hash_doc(doc_text):
        key = f"{doc_text.strip()}".encode()
        return hashlib.sha256(key).hexdigest()

    @staticmethod
    def _load_cache():
        return json.load(open(CACHE_FILE)) if os.path.exists(CACHE_FILE) else {}

    @staticmethod
    def _save_cache(cache):
        json.dump(cache, open(CACHE_FILE, "w"), indent=2)

