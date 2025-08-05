# main.py (FastAPI backend)

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Initialize backend components
graph = MemoryGraph()
vector = VectorIndex()
store = MemoryStore()
loader = MemoryLoader(store)
extractor = MemoryExtractor()
tracer = ThoughtTracer()
reasoner = ReasoningEngine(graph)

# Load graph from persistent store
loader.load_to_graph(graph)

class MemoryInput(BaseModel):
    text: str

@app.post("/add")
def add_conversation(payload: MemoryInput):
    text = payload.text
    extracted = extractor.extract(text)
    for item in extracted:
        topic = item.get("topic", "unknown")
        summary = item.get("summary", [])
        if not isinstance(summary, list):
            summary = [summary]
        for s in summary:
            graph.add_memory("User", "has_trait", topic, metadata={"summary": s})
            vector.add_entry(s, meta={"topic": topic, "summary": s})
            tracer.log(f"Added trait {topic}", s)
    loader.save_from_graph(graph)
    return {"status": "success", "extracted": extracted}

@app.get("/graph")
def get_graph():
    nodes = []
    edges = []
    for node, data in graph.graph.nodes(data=True):
        nodes.append({"id": node, "label": node, **data})
    for u, v, data in graph.graph.edges(data=True):
        edges.append({"source": u, "target": v, "label": data.get("relation", "rel")})
    return {"nodes": nodes, "edges": edges}

@app.get("/search")
def search_memories(q: str = Query(...)):
    results = vector.similarity_search(q)
    return results
