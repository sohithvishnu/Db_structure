
# persona_graph_memory/reasoning/inference.py

class ReasoningEngine:
    def __init__(self, graph):
        self.graph = graph

    def update_belief(self, entity, new_trait, contradicts=None):
        if contradicts:
            for neighbor, edge in self.graph.get_related(entity):
                if edge.get("relation") == "has_trait" and neighbor == contradicts:
                    edge["expired"] = True
        self.graph.add_memory(entity, "has_trait", new_trait, metadata={"updated": True})