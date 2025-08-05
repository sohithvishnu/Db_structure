
# persona_graph_memory/io/extractor.py

import json
import requests

class MemoryExtractor:
    def __init__(self, model="llama3.2"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def extract(self, text):
        system_prompt = """
You are a memory builder. Extract key user-specific facts from the following conversation.
Focus on preferences, personality traits, future plans, beliefs, and evolving information.
Respond in JSON format like this:
[
  {"topic": "travel", "summary": "User plans to visit Japan in September."},
  {"topic": "diet", "summary": "User follows a vegetarian diet."}
]"""
        prompt = system_prompt + "\n\n" + text
        res = requests.post(self.url, json={"model": self.model, "prompt": prompt, "stream": False})
        return json.loads(res.json().get("response", "[]"))
