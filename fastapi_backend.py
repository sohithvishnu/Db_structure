# main.py (FastAPI backend with instance-based persona graphs)

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import os

from db.graph import MemoryGraph
from db.vector import VectorIndex
from db.storage import MemoryStore
from db.io.loader import MemoryLoader
from db.io.extractor import MemoryExtractor
from reasoning.trace import ThoughtTracer
from reasoning.inference import ReasoningEngine

app = FastAPI()

# Enable CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Central registries for entity-specific instances
graphs: Dict[str, MemoryGraph] = {}
vectors: Dict[str, VectorIndex] = {}
loaders: Dict[str, MemoryLoader] = {}
tracers: Dict[str, ThoughtTracer] = {}
reasoners: Dict[str, ReasoningEngine] = {}
store = MemoryStore()
extractor = MemoryExtractor()

class MemoryInput(BaseModel):
    entity: str
    text: str
    fresh: bool = False  # optional flag to start a fresh instance

def init_instance(entity: str, fresh: bool = False):
    if fresh and entity in graphs:
        del graphs[entity]
        del vectors[entity]
        del loaders[entity]
        del tracers[entity]
        del reasoners[entity]

    if entity not in graphs:
        graph = MemoryGraph()
        vector = VectorIndex()
        tracer = ThoughtTracer()
        reasoner = ReasoningEngine(graph)
        loader = MemoryLoader(store)
        loader.load_to_graph(graph)

        graphs[entity] = graph
        vectors[entity] = vector
        loaders[entity] = loader
        tracers[entity] = tracer
        reasoners[entity] = reasoner

@app.post("/add")
def add_conversation(payload: MemoryInput):
    entity = payload.entity
    text = payload.text
    fresh = payload.fresh
    init_instance(entity, fresh=fresh)

    graph = graphs[entity]
    vector = vectors[entity]
    tracer = tracers[entity]
    loader = loaders[entity]

    extracted = extractor.extract(text)
    print(f"📥 Extracted {len(extracted)} memory items for '{entity}'")

    for item in extracted:
        topic = item.get("topic", "unknown")
        summary = item.get("summary", [])
        if not isinstance(summary, list):
            summary = [summary]
        for s in summary:
            graph.add_memory(entity, "has_trait", topic, metadata={"summary": s})
            vector.add_entry(s, meta={"topic": topic, "summary": s, "entity": entity})
            tracer.log(f"{entity} has_trait {topic}", s)

    loader.save_from_graph(graph)
    return {"status": "success", "extracted": extracted}

@app.get("/graph")
def get_graph(entity: str = Query(...)):
    init_instance(entity)
    graph = graphs[entity]
    nodes = []
    edges = []
    for node, data in graph.graph.nodes(data=True):
        nodes.append({"id": node, "label": node, **data})
    for u, v, data in graph.graph.edges(data=True):
        edges.append({"source": u, "target": v, "label": data.get("relation", "rel")})
    return {"nodes": nodes, "edges": edges}

@app.get("/search")
def search_memories(q: str = Query(...), entity: str = Query(...)):
    init_instance(entity)
    vector = vectors[entity]

    if vector.index is None or vector.index.ntotal == 0:
        print(f"⚠️ No vector index available for '{entity}' — skipping search.")
        return []

    results = vector.similarity_search(q)
    return results

@app.post("/clear")
def clear_entity(entity: str = Query(...)):
    if entity in graphs:
        del graphs[entity]
        del vectors[entity]
        del loaders[entity]
        del tracers[entity]
        del reasoners[entity]
        return {"status": f"Memory for '{entity}' cleared."}
    return {"status": f"Entity '{entity}' does not exist."}
