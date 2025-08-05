from db.storage import MemoryStore
from db.graph import MemoryGraph
from db.vector import VectorIndex
from db.io.extractor import MemoryExtractor
from db.io.loader import MemoryLoader
from reasoning.explain import ExplanationEngine
from reasoning.inference import ReasoningEngine
from reasoning.trace import ThoughtTracer


# Initialize components
graph = MemoryGraph()
vector = VectorIndex()
store = MemoryStore("persona_memory.json")
extractor = MemoryExtractor()
loader = MemoryLoader(store)
tracer = ThoughtTracer()
explainer = ExplanationEngine(tracer)
reasoner = ReasoningEngine(graph)

# 1. Extract memory from raw text
conversation = """
Michel said he enjoys hiking and dislikes crowds. Recently, he signed up for a solo trek in the Alps.
He also mentioned he's vegetarian and meditates every morning.
"""

extracted = extractor.extract(conversation)
print("\n🔍 Extracted memory entries:", extracted)

# 2. Add extracted memory to graph + vector store
for item in extracted:
    topic = item.get("topic", "unknown")
    summaries = item.get("summary", [])
    if not isinstance(summaries, list):
        summaries = [summaries]

    for summary in summaries:
        graph.add_memory("Michel", "has_trait", topic, metadata={"summary": summary})
        vector.add_entry(summary, meta={"topic": topic, "summary": summary})
        tracer.log(f"Added trait {topic}", summary)

# 3. Add reasoning / belief update
reasoner.update_belief("Michel", "outdoorsy", contradicts="indoorsy")
tracer.log("Michel is outdoorsy", "He signed up for a trek and enjoys hiking")

# 4. Save memory to disk
loader.save_from_graph(graph)

# 5. Reload and search
print("\n💾 Reloading from memory store...")
loader.load_to_graph(graph)
results = vector.similarity_search("Michel enjoys nature", k=3)

print("\n🔎 Similar memory results:")
for r in results:
    print("-", r["summary"])

# 6. Explain system conclusions
print("\n📘 Reasoning Explanation:")
for line in explainer.from_trace():
    print("•", line)
