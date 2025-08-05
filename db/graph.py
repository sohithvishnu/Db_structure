# persona_graph_memory/db/graph.py

import networkx as nx
from datetime import datetime
import uuid

class MemoryGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def _generate_id(self):
        return str(uuid.uuid4())

    def add_entity(self, name, entity_type="person"):
        self.graph.add_node(name, type=entity_type)

    def add_memory(self, entity, relation, target, metadata=None):
        metadata = metadata or {}
        for key in ["relation", "timestamp"]:
            if key in metadata:
                metadata.pop(key)
        if entity not in self.graph:
            self.add_entity(entity)
        if target not in self.graph:
            self.add_entity(target, entity_type=metadata.get("target_type", "concept"))
        self.graph.add_edge(entity, target, relation=relation, timestamp=datetime.now().isoformat(), **metadata)

    def get_related(self, entity, relation=None):
        neighbors = []
        for neighbor in self.graph.neighbors(entity):
            edge_data = self.graph.get_edge_data(entity, neighbor)
            if relation is None or edge_data.get("relation") == relation:
                neighbors.append((neighbor, edge_data))
        return neighbors