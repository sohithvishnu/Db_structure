# persona_graph_memory/io/loader.py

class MemoryLoader:
    def __init__(self, store):
        self.store = store

    def load_to_graph(self, graph):
        data = self.store.load()
        for entry in data:
            graph.add_memory(entry["entity"], entry.get("relation", "has_trait"), entry["value"], metadata=entry)

    def save_from_graph(self, graph):
        data = []
        for u, v, d in graph.graph.edges(data=True):
            entry = {"entity": u, "value": v, "relation": d.get("relation"), **d}
            data.append(entry)
        self.store.save(data)
