import networkx as nx
import re
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_references(text):
    """Extracts section references like 4.3.2 from text"""
    return re.findall(r"\b(\d+\.\d+(?:\.\d+)*)\b", text)

def normalize_section_id(sid):
    return sid.split("\t")[0].strip()

def get_neighbors(section_id, all_ids):
    """Returns parent, siblings, and children of a section ID"""
    parts = section_id.split(".")
    parent = ".".join(parts[:-1]) if len(parts) > 1 else None

    children = [
        sid for sid in all_ids if sid.startswith(section_id + ".")
    ]

    siblings = [
        sid for sid in all_ids
        if sid != section_id and sid.split(".")[:-1] == parts[:-1]
    ]

    return {
        "parent": parent if parent in all_ids else None,
        "siblings": sorted(siblings),
        "children": sorted(children),
    }

def build_semantic_graph(sections_10: dict, sections_17: dict):
    """
    Builds ONE graph with change info encoded in node attributes.
    - If section only in rel10 → removed
    - If only in rel17 → added
    - If in both → compare embeddings
    """
    G = nx.DiGraph()

    norm_10 = {normalize_section_id(k): v for k, v in sections_10.items()}
    norm_17 = {normalize_section_id(k): v for k, v in sections_17.items()}

    all_section_ids = set(norm_10) | set(norm_17)

    for sid in all_section_ids:
        old_text = sections_10.get(sid, "").strip()
        new_text = sections_17.get(sid, "").strip()

        node_attrs = {"section_id": sid}

        if not old_text and new_text:
            node_attrs["type"] = "added"
            node_attrs["text"] = new_text
        elif old_text and not new_text:
            node_attrs["type"] = "removed"
            node_attrs["text"] = old_text
        elif old_text and new_text:
            sim = util.cos_sim(model.encode(old_text), model.encode(new_text)).item()
            if sim < 0.85:
                node_attrs["type"] = "modified"
                node_attrs["similarity"] = round(sim, 3)
                node_attrs["old_text"] = old_text
                node_attrs["new_text"] = new_text
                node_attrs["text"] = new_text
            else:
                node_attrs["type"] = "unchanged"
                node_attrs["text"] = new_text

        G.add_node(sid, **node_attrs)

        # Add mention-based edges
        source_text = new_text or old_text or ""
        for ref in extract_references(source_text):
            if ref != sid:
                G.add_edge(sid, ref, reason="mentions")

    # Add neighbors to each node
    for sid in G.nodes:
        G.nodes[sid]["neighbors"] = get_neighbors(sid, all_section_ids)

    return G


def build_graph_from_sections(sections: dict):
    """
    Builds a simple directed graph from sections of a single version.
    Nodes contain section_id and text.
    Edges are added for section references (e.g., mentions of 4.2.1 in 5.3).
    """
    G = nx.DiGraph()

    for sid, text in sections.items():
        norm_id = normalize_section_id(sid)
        G.add_node(norm_id, section_id=norm_id, text=text.strip())

        for ref in extract_references(text):
            if ref != norm_id:
                G.add_edge(norm_id, ref, reason="mentions")

    return G