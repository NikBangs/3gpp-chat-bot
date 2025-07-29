import pickle
from graphs.traversals import inspect_node
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
graph_path = project_root / "data" / "unified_graph.pkl"

with open(graph_path, "rb") as f:
    G = pickle.load(f)

print("\n📚 Sample node IDs in the graph:")
sample_ids = list(G.nodes)[:10]
print(sample_ids)

# Change this to the section ID you want to inspect
section_to_check = "9.9.3"
inspect_node(G, section_to_check)