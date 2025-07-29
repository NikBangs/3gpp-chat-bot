from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pathlib as Path
import os
import networkx as nx
import pickle
import json

app = Flask(__name__)
CORS(app)

# Load graph
with open(os.path.join(os.path.dirname(__file__), "../data/unified_graph.pkl"), "rb") as f:
    G = pickle.load(f)

# Build documents
documents = []
node_ids = []

for node_id, data in G.nodes(data=True):
    title = data.get("title", "")
    text = data.get("text", "")
    change_type = data.get("type", "")

    # Prefer summarizer title if available
    combined_text = f"{title} {text} {change_type}"
    documents.append(combined_text)
    node_ids.append(node_id)


# TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(documents)

@app.route("/api/query", methods=["POST"])
def query():
    try:
        data = request.get_json(force=True)  # <— ensures JSON is parsed even if headers are off
        print("Received data from frontend:", data)

        query_text = data.get("query", "").strip().lower()
        if not query_text:
            return jsonify({"answer": "Please enter a valid question.", "highlight": []})

        results = []
        highlights = []

        for node_id, attr in G.nodes(data=True):
            content = (attr.get("text", "") + " " + attr.get("title", "")).lower()
            if query_text in content:
                highlights.append(node_id)

                # Start with current node's text
                section_text = f"🔹 {attr.get('title', node_id)}: {attr.get('text', '')}"

                # Fetch neighbor info
                neighbors = attr.get("neighbors", {})
                neighbor_ids = neighbors.get("parent", []) + neighbors.get("siblings", []) + neighbors.get("children", [])

                neighbor_snippets = []
                for n_id in neighbor_ids:
                    n_data = G.nodes.get(n_id, {})
                    if not n_data:
                        continue
                    n_title = n_data.get("title", n_id)
                    n_text = n_data.get("text", "")
                    if n_text:
                        snippet = f"   ↪ {n_title}: {n_text[:300]}{'...' if len(n_text) > 300 else ''}"
                        neighbor_snippets.append(snippet)

                full_response = section_text + "\n\n" + "\n".join(neighbor_snippets)
                results.append(full_response)

        if not results:
            return jsonify({"answer": "Sorry, I couldn't find anything.", "highlight": []})

        return jsonify({
            "answer": "\n\n---\n\n".join(results),
            "highlight": highlights,
        })

    except Exception as e:
        print("Error processing query:", e)
        return jsonify({"answer": "Server error occurred.", "highlight": []}), 500

@app.route('/api/graph', methods=['GET'])
def get_graph():
    filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'unified_graph.pkl')
    filepath = os.path.abspath(filepath)

    with open(filepath, "rb") as f:
        data = pickle.load(f)
    
    # convert to JSON-serializable format (for frontend)
    graph_data = {
        "nodes": [{"id": str(node)} for node in data.nodes()],
        "links": [{"source": str(u), "target": str(v)} for u, v in data.edges()]
    }
    return jsonify(graph_data)

if __name__ == "__main__":
    app.run(debug=True)
