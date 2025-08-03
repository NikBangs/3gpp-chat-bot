from pathlib import Path
import json
import pickle
import networkx as nx
import os
import sys

# --- Project modules ---
from parser.read_doc import read_doc
from parser.split_sections import split_docx_into_sections, split_text_into_sections 
from graphs.builder import build_semantic_graph, build_graph_from_sections
from graphs.visualizer import visualize_semantic_graph, export_to_html
from graphs.traversals import downstream_impact
from graphs.summarizer import generate_user_friendly_summary

BASE_DIR = Path(__file__).resolve().parent.parent  # Goes up to 3GPP Chat Bot/
FRONTEND_PUBLIC_DATA_DIR = BASE_DIR / "frontend" / "public" / "data"
DATA_DIR = BASE_DIR / "data"
GRAPH_DIR = DATA_DIR / "graphs"
VIEW_DIR = DATA_DIR / "graph_views"

def sanitize_keys(data):
    return {str(k): v for k, v in data.items()}

def write_changes_json(changes, path="data/changes.json"):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sanitize_keys(changes), f, indent=2)
        print(f"📝 {len(changes)} changed sections saved to {path}")
    except Exception as e:
        print(f"❌ Failed to write changes.json: {e}")

def launch_graph_gui():
    import subprocess
    script_dir = Path(__file__).resolve().parent
    gui_script = script_dir / "ui" / "run_graph_gui.py"

    if gui_script.exists():
        print("🪟 Launching Graph Viewer App...")
        return_code = subprocess.call([sys.executable, str(gui_script)])
        if return_code == 0:
            print("👋 GUI closed.")
        else:
            print(f"⚠️ GUI exited with code {return_code}")
    else:
        print(f"❌ GUI script not found at: {gui_script}")

def load_cached_graph(graph_path):
    print("📂 Loading cached graph...")
    with open(graph_path, "rb") as f:
        return pickle.load(f)

def flatten_section(section):
    if not section or not isinstance(section, dict) or "content" not in section:
        return ""
    return " ".join(entry.get("text", "") for entry in section["content"])

def normalize_keys(d):
    return {k.split("\t")[0].strip(): v for k, v in d.items()}

def main():
    rel10_path = DATA_DIR / "24301-af0.doc"
    rel17_path = DATA_DIR / "24301-hc0.docx"
    graph_path = DATA_DIR / "unified_graph.pkl"
    changes_path = DATA_DIR / "changes.json"

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(GRAPH_DIR, exist_ok=True)
    os.makedirs(VIEW_DIR, exist_ok=True)

    # -------- Cached Mode --------
    if graph_path.exists() and changes_path.exists():
        print("✅ Using cached graph and changes.json.")
        G = load_cached_graph(graph_path)
        with open(changes_path, "r", encoding="utf-8") as f:
            changes = json.load(f)

        try:
            print("📄 Re-reading documents for tooltip rendering and fallback graph generation...")
            text10 = read_doc(rel10_path)
            sections10_raw = split_text_into_sections(text10)
            sections17_raw = split_docx_into_sections(rel17_path)

            sections10 = normalize_keys(sections10_raw)
            sections17 = normalize_keys(sections17_raw)

            # 🔁 Build individual graphs if missing
            graph10_path = GRAPH_DIR / "graph_10.pkl"
            graph17_path = GRAPH_DIR / "graph_17.pkl"
            html10_path = VIEW_DIR / "graph_10.html"
            html17_path = VIEW_DIR / "graph_17.html"

            if not graph10_path.exists() or not graph17_path.exists():
                print("🔄 Individual version graph .pkl files missing. Rebuilding...")
                flattened10 = {sid: flatten_section(sec) for sid, sec in sections10.items()}
                flattened17 = {sid: flatten_section(sec) for sid, sec in sections17.items()}

                graph10 = build_graph_from_sections(flattened10)
                graph17 = build_graph_from_sections(flattened17)

                with open(graph10_path, "wb") as f:
                    pickle.dump(graph10, f)
                with open(graph17_path, "wb") as f:
                    pickle.dump(graph17, f)

                print("✅ Individual .pkl graphs saved.")

            if not html10_path.exists() or not html17_path.exists():
                print("🔄 HTML graph views missing. Regenerating...")
                if 'graph10' not in locals():
                    flattened10 = {sid: flatten_section(sec) for sid, sec in sections10.items()}
                    graph10 = build_graph_from_sections(flattened10)
                if 'graph17' not in locals():
                    flattened17 = {sid: flatten_section(sec) for sid, sec in sections17.items()}
                    graph17 = build_graph_from_sections(flattened17)

                export_to_html(graph10, html10_path, title="3GPP Rel-10 Graph")
                export_to_html(graph17, html17_path, title="3GPP Rel-17 Graph")
                print("✅ Individual HTML graph views saved.")
        except Exception as e:
            print(f"❌ Failed to re-read documents for visualization: {e}")
            return
    else:
        # -------- Document Check --------
        if not rel10_path.exists():
            print(f"❌ File not found: {rel10_path}")
            return
        if not rel17_path.exists():
            print(f"❌ File not found: {rel17_path}")
            return

        # -------- Read and Parse --------
        print("📄 Reading documents...")
        try:
            text10 = read_doc(rel10_path)
            text17 = read_doc(rel17_path)
        except Exception as e:
            print(f"❌ Failed to read documents: {e}")
            return

        print("🔍 Splitting into structured sections...")
        sections10_raw = split_text_into_sections(text10)       # .doc → plain text
        sections17_raw = split_docx_into_sections(rel17_path)   # .docx → structured

        sections10 = normalize_keys(sections10_raw)
        sections17 = normalize_keys(sections17_raw)

        # -------- Flatten for Semantic Graph --------
        print("🧠 Building unified semantic graph...")
        flattened10 = {sid: flatten_section(sec) for sid, sec in sections10.items()}
        flattened17 = {sid: flatten_section(sec) for sid, sec in sections17.items()}

        G = build_semantic_graph(flattened10, flattened17)

        print(f"✅ Graph built with {len(G.nodes)} nodes and {len(G.edges)} edges.")

        # -------- Individual Version Graphs --------
        graph10 = build_graph_from_sections(flattened10)
        graph17 = build_graph_from_sections(flattened17)

        with open(GRAPH_DIR / "graph_10.pkl", "wb") as f:
            pickle.dump(graph10, f)
        with open(GRAPH_DIR / "graph_17.pkl", "wb") as f:
            pickle.dump(graph17, f)

        export_to_html(graph10, VIEW_DIR / "graph_10.html", title="3GPP Rel-10 Graph")
        export_to_html(graph17, VIEW_DIR / "graph_17.html", title="3GPP Rel-17 Graph")
        print("📦 Individual version graphs saved in 'graphs/' and visualized in 'graph_views/'")

        # -------- Summarize Nodes with GPT --------
        try:
            from graphs.summarize_nodes import summarize_graph_nodes
            G = summarize_graph_nodes(G)

            # Re-save enriched graph
            with open(graph_path, "wb") as f:
                pickle.dump(G, f)
            print("🧠 Node summaries added and saved.")
        except Exception as e:
            print(f"⚠️ Skipped summarization due to error: {e}")

        # -------- Save Graph and Changes --------
        with open(graph_path, "wb") as f:
            pickle.dump(G, f)
        print("💾 Graph saved to", graph_path)

        changes = {
            sid: data for sid, data in G.nodes(data=True)
            if data.get("type") != "unchanged"
        }
        write_changes_json(changes, changes_path)

    # -------- Visualization --------
    print("🌐 Generating interactive visualization...")
    data_output_path = DATA_DIR / "graph.html"
    frontend_output_path = FRONTEND_PUBLIC_DATA_DIR / "graph.html"
    visualize_semantic_graph(G, output_html=str(data_output_path), sections10=sections10, sections17=sections17)
    visualize_semantic_graph(G, output_html=str(frontend_output_path), sections10=sections10, sections17=sections17)
    print("🎉 Visualization saved to graph.html")

    # -------- Optional: Impact Test --------
    test_section = "4.3.2"
    if test_section in G:
        impacted = downstream_impact(G, test_section)
        print(f"📌 Sections impacted by change in {test_section}:", impacted)
    else:
        print(f"⚠️ Section {test_section} not found in graph.")

    # -------- Optional: QA Summary --------
    section_id = input("🔎 Enter a section ID to explain (e.g., 5.2.1): ").strip()
    if section_id:
        explanation = generate_user_friendly_summary(G, section_id)
        print("\n📝 Explanation:\n")
        print(explanation)

    # -------- GUI Viewer --------
    launch_graph_gui()

if __name__ == "__main__":
    main()
