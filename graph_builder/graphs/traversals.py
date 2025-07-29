import networkx as nx

def downstream_impact(graph: nx.DiGraph, section_id: str, depth=2):
    """
    Returns a list of nodes affected by a section, up to `depth` hops away.
    E.g. "If 4.3.2 is modified, which sections depend on it?"
    """
    impacted = set()
    for d in range(1, depth + 1):
        impacted |= nx.descendants_at_distance(graph, section_id, d)
    return list(impacted)

def inspect_node(graph: nx.DiGraph, section_id: str):
    """Prints node attributes for easy debugging"""
    if section_id in graph.nodes:
        node = graph.nodes[section_id]
        print(f"\n🔍 Section {section_id}")
        for k, v in node.items():
            if isinstance(v, str) and len(v) > 300:
                print(f"{k}: {v[:300]}...")  # preview large text
            else:
                print(f"{k}: {v}")
    else:
        print(f"❌ Section {section_id} not found in graph.")