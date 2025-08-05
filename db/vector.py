
# persona_graph_memory/db/vector.py

from langchain_ollama import OllamaEmbeddings
import faiss
import numpy as np

class VectorIndex:
    def __init__(self, model="llama3.2"):
        self.embedder = OllamaEmbeddings(model=model)
        self.index = None # Assuming 1024-dim vectors
        self.vectors = []
        self.metadata = []

    def add_entry(self, text, meta):
        vec = self.embedder.embed_query(text)
        vec_np = np.array(vec).astype("float32").reshape(1, -1)

         # Initialize the index with correct dimensionality
        if self.index is None:
            dim = vec_np.shape[1]
            self.index = faiss.IndexFlatL2(dim)

        self.index.add(vec_np)
        self.vectors.append(vec_np)
        self.metadata.append(meta)

    def similarity_search(self, query, k=5):
        if self.index is None or self.index.ntotal == 0:
            return []
        query_vec = self.embedder.embed_query(query)
        D, I = self.index.search(query_vec, k)
        results = []
        for idx in I[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results

