
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

    def similarity_search(self, text, k=5):
        query_vec = np.array(self.embedder.embed_query(text)).astype("float32").reshape(1, -1)
        D, I = self.index.search(query_vec, k)
        return [self.metadata[i] for i in I[0] if i < len(self.metadata)]
