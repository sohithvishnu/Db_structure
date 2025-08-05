
# persona_graph_memory/db/storage.py

import json
import os

class MemoryStore:
    def __init__(self, filepath="memory_store.json"):
        self.filepath = filepath

    def save(self, memory_list):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(memory_list, f, indent=2)

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []