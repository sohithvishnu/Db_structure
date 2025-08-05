import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Persona Graph Memory", layout="wide")
st.title("🧠 Persona Graph Memory Viewer")

# Section 0: Entity name input
entity_name = st.text_input("🧠 Enter Persona Name", value="Michel")

# Section 1: Add new memory input
st.markdown("### 📝 Add New Conversation")
user_input = st.text_area("Paste user conversation:", height=150)

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Process and Add to Memory"):
        response = requests.post(f"{API_URL}/add", json={
            "entity": entity_name,
            "text": user_input,
            "fresh": True
        })
        if response.status_code == 200:
            st.success("Memory added successfully!")
        else:
            st.error("Failed to add memory.")

with col2:
    if st.button("🧹 Clear Memory for This Persona"):
        clear_res = requests.post(f"{API_URL}/clear", params={"entity": entity_name})
        if clear_res.status_code == 200:
            st.success(clear_res.json().get("status"))
        else:
            st.error("Failed to clear memory.")

st.divider()

# Section 2: Graph Visualization
st.markdown("### 🕸️ Memory Graph")
res = requests.get(f"{API_URL}/graph", params={"entity": entity_name})
if res.status_code != 200:
    st.error("Failed to fetch graph from API")
    st.stop()

graph_data = res.json()
G = nx.DiGraph()

for node in graph_data["nodes"]:
    G.add_node(node["id"], label=node["label"], type=node.get("type", ""))

for edge in graph_data["edges"]:
    G.add_edge(edge["source"], edge["target"], label=edge["label"])

fig, ax = plt.subplots(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)

node_labels = {n: d["label"] for n, d in G.nodes(data=True)}
edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}

nx.draw(G, pos, with_labels=False, node_size=1000, node_color="#d0e1f9", edge_color="#888888", ax=ax)
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, ax=ax)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)

st.pyplot(fig)

# Section 3: Semantic search
st.markdown("### 🔍 Semantic Memory Search")
query = st.text_input("Search memories semantically")
if query:
    res = requests.get(f"{API_URL}/search", params={"q": query, "entity": entity_name})
    if res.status_code == 200:
        results = res.json()
        for r in results:
            st.info(f"**{r['topic']}**: {r['summary']}")
    else:
        st.error("Search failed")
