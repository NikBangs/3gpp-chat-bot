import networkx as nx

def generate_user_friendly_summary(graph: nx.DiGraph, start_node: str, max_depth=2):
    """
    Generates a natural-language explanation for changes starting from a given section ID.
    Traverses the graph up to `max_depth` to capture related changes.
    """
    if start_node not in graph.nodes:
        return f"❌ Section {start_node} not found in the graph."

    summary = []
    visited = set()
    queue = [(start_node, 0)]

    emoji_map = {
        "added": "➕",
        "removed": "❌",
        "modified": "📌",
        "unchanged": "✅"
    }

    while queue:
        node, depth = queue.pop(0)
        if node in visited or depth > max_depth:
            continue
        visited.add(node)

        data = graph.nodes[node]
        change_type = data.get("type", "unchanged")
        short_text = data.get("text", "").strip().replace("\n", " ")
        if len(short_text) > 200:
            short_text = short_text[:200] + "..."

        emoji = emoji_map.get(change_type, "🔹")
        summary.append(f"{emoji} Section {node} ({change_type}):\n → {short_text}\n")

        for neighbor in graph.neighbors(node):
            queue.append((neighbor, depth + 1))

    return "\n".join(summary)
